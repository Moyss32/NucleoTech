import logging
from rest_framework.permissions import BasePermission
from django.utils import timezone
from .models import UsuarioAssinatura

logger = logging.getLogger(__name__)


class IsActiveSubscriber(BasePermission):
    """
    Allows access only to users with an active paid subscription.
    """
    message = 'É necessária uma assinatura ativa para acessar este recurso.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            ua = request.user.assinatura_perfil
            return ua.is_active_subscriber
        except UsuarioAssinatura.DoesNotExist:
            logger.warning(
                f"Usuário {request.user.id} tentou acessar recurso premium sem assinatura registrada."
            )
            return False


class HasUpscaleAccess(BasePermission):
    """
    Allows access only to subscribers whose plan includes upscale.
    """
    message = 'O serviço de upscale não está disponível no seu plano atual.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            ua = request.user.assinatura_perfil
            return ua.is_active_subscriber and ua.acesso_upscale
        except UsuarioAssinatura.DoesNotExist:
            return False


class HasDailyQuota(BasePermission):
    """
    Checks daily usage quota. Resets counter if a new day has started.
    """
    message = 'Você atingiu o limite diário de processamentos do seu plano.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            ua = request.user.assinatura_perfil
            # Reset daily usage if needed
            today = timezone.now().date()
            if ua.data_ultimo_reset_diario != today:
                ua.uso_diario_atual = 0
                ua.data_ultimo_reset_diario = today
                ua.save(update_fields=['uso_diario_atual', 'data_ultimo_reset_diario'])

            return ua.uso_diario_atual < ua.limite_diario
        except UsuarioAssinatura.DoesNotExist:
            return False


class HasMonthlyQuota(BasePermission):
    """
    Checks monthly usage quota.
    """
    message = 'Você atingiu o limite mensal de processamentos do seu plano.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            ua = request.user.assinatura_perfil
            return ua.uso_atual < ua.limite_mensal
        except UsuarioAssinatura.DoesNotExist:
            return False
