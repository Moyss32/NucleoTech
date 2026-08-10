"""
Stripe service layer — centralizes all Stripe API interactions and
database state updates related to subscriptions and payments.
"""
import logging
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import datetime

from .models import Assinatura, UsuarioAssinatura, HistoricoPagamento

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Customer helpers
# ---------------------------------------------------------------------------

def get_or_create_stripe_customer(user: User) -> str:
    """
    Returns the Stripe customer_id for the user, creating one if needed.
    """
    ua, _ = UsuarioAssinatura.objects.get_or_create(usuario=user)

    if ua.stripe_customer_id:
        return ua.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        name=user.get_full_name() or user.username,
        metadata={'user_id': user.id},
    )
    ua.stripe_customer_id = customer.id
    ua.save(update_fields=['stripe_customer_id'])
    logger.info(f"Stripe customer created: {customer.id} for user {user.id}")
    return customer.id


# ---------------------------------------------------------------------------
# Checkout
# ---------------------------------------------------------------------------

def create_checkout_session(user: User, plano: Assinatura, success_url: str, cancel_url: str) -> dict:
    """
    Creates a Stripe Checkout Session for a subscription plan.
    Returns {'sessionId': ..., 'url': ...}
    """
    if not plano.stripe_price_id:
        raise ValueError('Este plano não possui um ID de preço do Stripe configurado.')

    customer_id = get_or_create_stripe_customer(user)

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=['card'],
        line_items=[{'price': plano.stripe_price_id, 'quantity': 1}],
        mode='subscription',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            'user_id': str(user.id),
            'plano_id': str(plano.id),
        },
        subscription_data={
            'metadata': {
                'user_id': str(user.id),
                'plano_id': str(plano.id),
            }
        },
    )
    logger.info(f"Checkout session {session.id} created for user {user.id}, plan {plano.id}")
    return {'sessionId': session.id, 'url': session.url}


# ---------------------------------------------------------------------------
# Portal (customer self-service)
# ---------------------------------------------------------------------------

def create_portal_session(user: User, return_url: str) -> str:
    """
    Creates a Stripe Billing Portal session for the user.
    Returns the portal URL.
    """
    customer_id = get_or_create_stripe_customer(user)
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return session.url


# ---------------------------------------------------------------------------
# Webhook handlers
# ---------------------------------------------------------------------------

def handle_checkout_session_completed(session: dict):
    """checkout.session.completed"""
    user_id = session.get('metadata', {}).get('user_id')
    plano_id = session.get('metadata', {}).get('plano_id')

    if not user_id or not plano_id:
        logger.error(f"checkout.session.completed missing metadata: {session.get('id')}")
        return

    try:
        user = User.objects.get(id=user_id)
        plano = Assinatura.objects.get(id=plano_id)
    except (User.DoesNotExist, Assinatura.DoesNotExist) as e:
        logger.error(f"checkout.session.completed - entity not found: {e}")
        return

    ua, _ = UsuarioAssinatura.objects.get_or_create(usuario=user)
    ua.plano = plano
    ua.stripe_customer_id = session.get('customer') or ua.stripe_customer_id
    ua.stripe_subscription_id = session.get('subscription') or ua.stripe_subscription_id
    ua.status_assinatura = 'active'
    ua.save()
    logger.info(f"Subscription activated for user {user.id} via checkout session {session.get('id')}")


def handle_subscription_created(subscription: dict):
    """customer.subscription.created"""
    _sync_subscription(subscription)


def handle_subscription_updated(subscription: dict):
    """customer.subscription.updated"""
    _sync_subscription(subscription)


def handle_subscription_deleted(subscription: dict):
    """customer.subscription.deleted"""
    try:
        ua = UsuarioAssinatura.objects.get(stripe_subscription_id=subscription['id'])
        ua.status_assinatura = 'canceled'
        ua.plano = None
        ua.save(update_fields=['status_assinatura', 'plano'])
        logger.info(f"Subscription {subscription['id']} canceled for user {ua.usuario_id}")
    except UsuarioAssinatura.DoesNotExist:
        logger.warning(f"customer.subscription.deleted — UsuarioAssinatura not found for sub {subscription['id']}")


def handle_invoice_paid(invoice: dict):
    """invoice.paid — records successful payment and keeps subscription active."""
    customer_id = invoice.get('customer')
    subscription_id = invoice.get('subscription')

    try:
        ua = UsuarioAssinatura.objects.get(stripe_customer_id=customer_id)
    except UsuarioAssinatura.DoesNotExist:
        logger.warning(f"invoice.paid — UsuarioAssinatura not found for customer {customer_id}")
        return

    # Ensure subscription status is active
    if ua.status_assinatura != 'active':
        ua.status_assinatura = 'active'
        ua.save(update_fields=['status_assinatura'])

    # Record payment in history
    invoice_id = invoice.get('id', '')
    if invoice_id:
        paid_at = None
        if invoice.get('status_transitions', {}).get('paid_at'):
            paid_at = datetime.datetime.fromtimestamp(
                invoice['status_transitions']['paid_at'], tz=timezone.utc
            )

        HistoricoPagamento.objects.update_or_create(
            stripe_invoice_id=invoice_id,
            defaults={
                'usuario': ua.usuario,
                'assinatura_usuario': ua,
                'stripe_payment_intent_id': invoice.get('payment_intent'),
                'valor': (invoice.get('amount_paid', 0) or 0) / 100,
                'moeda': invoice.get('currency', 'brl'),
                'status': 'paid',
                'data_pagamento': paid_at or timezone.now(),
                'descricao': invoice.get('description') or f"Renovação de assinatura",
            }
        )
    logger.info(f"Invoice paid for customer {customer_id}, subscription {subscription_id}")


def handle_invoice_payment_failed(invoice: dict):
    """invoice.payment_failed — marks subscription as past_due."""
    customer_id = invoice.get('customer')

    try:
        ua = UsuarioAssinatura.objects.get(stripe_customer_id=customer_id)
        ua.status_assinatura = 'past_due'
        ua.save(update_fields=['status_assinatura'])

        invoice_id = invoice.get('id', '')
        if invoice_id:
            HistoricoPagamento.objects.update_or_create(
                stripe_invoice_id=invoice_id,
                defaults={
                    'usuario': ua.usuario,
                    'assinatura_usuario': ua,
                    'stripe_payment_intent_id': invoice.get('payment_intent'),
                    'valor': (invoice.get('amount_due', 0) or 0) / 100,
                    'moeda': invoice.get('currency', 'brl'),
                    'status': 'failed',
                    'descricao': 'Falha no pagamento da fatura.',
                }
            )
        logger.warning(f"Invoice payment failed for customer {customer_id}")
    except UsuarioAssinatura.DoesNotExist:
        logger.warning(f"invoice.payment_failed — UsuarioAssinatura not found for customer {customer_id}")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _sync_subscription(subscription: dict):
    """
    Syncs a Stripe subscription object to our UsuarioAssinatura model.
    Used by subscription.created and subscription.updated.
    """
    subscription_id = subscription.get('id')
    customer_id = subscription.get('customer')
    stripe_status = subscription.get('status', 'inactive')

    # Try to find by subscription_id first, then by customer_id
    ua = None
    try:
        ua = UsuarioAssinatura.objects.get(stripe_subscription_id=subscription_id)
    except UsuarioAssinatura.DoesNotExist:
        if customer_id:
            try:
                ua = UsuarioAssinatura.objects.get(stripe_customer_id=customer_id)
            except UsuarioAssinatura.DoesNotExist:
                logger.warning(f"_sync_subscription — no UsuarioAssinatura found for sub {subscription_id}")
                return

    if not ua:
        return

    ua.stripe_subscription_id = subscription_id
    ua.stripe_customer_id = customer_id or ua.stripe_customer_id
    ua.status_assinatura = stripe_status

    # Try to match plan from Stripe price id
    items = subscription.get('items', {}).get('data', [])
    if items:
        price_id = items[0].get('price', {}).get('id')
        if price_id:
            try:
                plano = Assinatura.objects.get(stripe_price_id=price_id)
                ua.plano = plano
            except Assinatura.DoesNotExist:
                logger.warning(f"_sync_subscription — no Assinatura found for price_id {price_id}")

    # Sync renewal date
    current_period_end = subscription.get('current_period_end')
    if current_period_end:
        ua.data_renovacao = datetime.datetime.fromtimestamp(current_period_end, tz=timezone.utc)

    ua.save()
    logger.info(f"Subscription {subscription_id} synced for user {ua.usuario_id} — status: {stripe_status}")
