from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Assinatura, UsuarioAssinatura
from .serializers import AssinaturaSerializer, UsuarioAssinaturaSerializer

class SubscriptionDetailView(generics.RetrieveAPIView):
    serializer_class = UsuarioAssinaturaSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        obj, created = UsuarioAssinatura.objects.get_or_create(usuario=self.request.user)
        return obj

class DashboardView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        ua, created = UsuarioAssinatura.objects.get_or_create(usuario=request.user)
        return Response({
            'plano': ua.plano.nome if ua.plano else 'Nenhum',
            'limite': ua.plano.limite_mensal if ua.plano else 0,
            'uso_atual': ua.uso_atual
        })
