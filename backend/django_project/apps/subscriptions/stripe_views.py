import logging
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from . import services

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    """
    POST /api/subscriptions/checkout/
    Body: { "plano_id": <int>, "success_url": "<url>", "cancel_url": "<url>" }
    Returns: { "sessionId": "...", "url": "..." }
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        from .models import Assinatura

        plano_id = request.data.get('plano_id')
        if not plano_id:
            return Response({'error': 'plano_id é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        # Allow frontend to pass URLs; fall back to settings
        success_url = request.data.get(
            'success_url',
            getattr(settings, 'STRIPE_SUCCESS_URL', request.build_absolute_uri('/payment/success/?session_id={CHECKOUT_SESSION_ID}'))
        )
        cancel_url = request.data.get(
            'cancel_url',
            getattr(settings, 'STRIPE_CANCEL_URL', request.build_absolute_uri('/payment/cancel/'))
        )

        try:
            plano = Assinatura.objects.get(id=plano_id, ativo=True)
        except Assinatura.DoesNotExist:
            return Response({'error': 'Plano não encontrado ou inativo.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = services.create_checkout_session(request.user, plano, success_url, cancel_url)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error during checkout for user {request.user.id}: {e}")
            return Response({'error': 'Erro ao comunicar com o Stripe. Tente novamente.'}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            logger.exception(f"Unexpected error during checkout for user {request.user.id}: {e}")
            return Response({'error': 'Erro interno do servidor.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StripeBillingPortalView(APIView):
    """
    POST /api/subscriptions/portal/
    Body: { "return_url": "<url>" }  (optional)
    Returns: { "url": "..." }
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        return_url = request.data.get(
            'return_url',
            request.build_absolute_uri('/user/dashboard/')
        )
        try:
            url = services.create_portal_session(request.user, return_url)
            return Response({'url': url}, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe portal error for user {request.user.id}: {e}")
            return Response({'error': 'Erro ao acessar o portal do Stripe.'}, status=status.HTTP_502_BAD_GATEWAY)


@csrf_exempt
def stripe_webhook(request):
    """
    POST /api/subscriptions/webhook/
    Handles all Stripe webhook events.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if not sig_header:
        logger.warning("Webhook received without Stripe-Signature header.")
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        logger.warning("Webhook: invalid payload received.")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.warning("Webhook: invalid signature received.")
        return HttpResponse(status=400)

    event_type = event['type']
    data_object = event['data']['object']

    logger.info(f"Stripe webhook received: {event_type} ({event.get('id')})")

    try:
        if event_type == 'checkout.session.completed':
            services.handle_checkout_session_completed(data_object)

        elif event_type == 'customer.subscription.created':
            services.handle_subscription_created(data_object)

        elif event_type == 'customer.subscription.updated':
            services.handle_subscription_updated(data_object)

        elif event_type == 'customer.subscription.deleted':
            services.handle_subscription_deleted(data_object)

        elif event_type in ('invoice.paid', 'invoice.payment_succeeded'):
            services.handle_invoice_paid(data_object)

        elif event_type == 'invoice.payment_failed':
            services.handle_invoice_payment_failed(data_object)

        else:
            logger.debug(f"Unhandled Stripe event type: {event_type}")

    except Exception as e:
        logger.exception(f"Error handling Stripe event {event_type} ({event.get('id')}): {e}")
        # Return 200 to prevent Stripe from retrying indefinitely for non-recoverable errors
        # For recoverable errors you may return 500
        return HttpResponse(status=200)

    return HttpResponse(status=200)
