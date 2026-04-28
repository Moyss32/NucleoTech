from rest_framework import serializers
from .models import Assinatura, UsuarioAssinatura

class AssinaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assinatura
        fields = '__all__'

class UsuarioAssinaturaSerializer(serializers.ModelSerializer):
    plano_nome = serializers.ReadOnlyField(source='plano.nome')
    limite_mensal = serializers.ReadOnlyField(source='plano.limite_mensal')
    
    class Meta:
        model = UsuarioAssinatura
        fields = ('plano_nome', 'limite_mensal', 'uso_atual', 'data_inicio')
