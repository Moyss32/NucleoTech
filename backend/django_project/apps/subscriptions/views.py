from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import Assinatura, UsuarioAssinatura, HistoricoPagamento
from .serializers import AssinaturaSerializer, UsuarioAssinaturaSerializer, HistoricoPagamentoSerializer


class SubscriptionListView(generics.ListAPIView):
    """
    GET /api/subscriptions/
    Lists all active subscription plans (public).
    """
    queryset = Assinatura.objects.filter(ativo=True).order_by('preco')
    serializer_class = AssinaturaSerializer
    permission_classes = (permissions.AllowAny,)


class SubscriptionDetailView(APIView):
    """
    GET /api/subscription/
    Returns the current user's subscription info.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ua, _ = UsuarioAssinatura.objects.get_or_create(usuario=request.user)

        # Reset daily usage if needed
        today = timezone.now().date()
        if ua.data_ultimo_reset_diario != today:
            ua.uso_diario_atual = 0
            ua.data_ultimo_reset_diario = today
            ua.save(update_fields=['uso_diario_atual', 'data_ultimo_reset_diario'])

        serializer = UsuarioAssinaturaSerializer(ua)
        return Response(serializer.data)


class DashboardView(APIView):
    """
    GET /api/user/dashboard/
    Returns enriched dashboard data for the authenticated user.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ua, _ = UsuarioAssinatura.objects.get_or_create(usuario=request.user)

        # Reset daily usage if needed
        today = timezone.now().date()
        if ua.data_ultimo_reset_diario != today:
            ua.uso_diario_atual = 0
            ua.data_ultimo_reset_diario = today
            ua.save(update_fields=['uso_diario_atual', 'data_ultimo_reset_diario'])

        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            },
            'plano': ua.plano.nome if ua.plano else None,
            'is_active_subscriber': ua.is_active_subscriber,
            'status_assinatura': ua.status_assinatura,
            'limite_mensal': ua.limite_mensal,
            'uso_mensal_atual': ua.uso_atual,
            'limite_diario': ua.limite_diario,
            'uso_diario_atual': ua.uso_diario_atual,
            'limite_tamanho_mb': ua.limite_tamanho_mb,
            'acesso_upscale': ua.acesso_upscale,
            'data_renovacao': ua.data_renovacao,
        })


class PaymentHistoryView(generics.ListAPIView):
    """
    GET /api/subscriptions/payments/
    Returns the authenticated user's payment history.
    """
    serializer_class = HistoricoPagamentoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return HistoricoPagamento.objects.filter(usuario=self.request.user)
