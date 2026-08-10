from rest_framework import serializers
from .models import Assinatura, UsuarioAssinatura, HistoricoPagamento


class AssinaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assinatura
        fields = [
            'id', 'nome', 'limite_mensal', 'limite_diario',
            'limite_tamanho_arquivo_mb', 'preco', 'descricao',
            'prioridade_fila', 'acesso_upscale', 'ativo',
            'stripe_price_id',
        ]


class UsuarioAssinaturaSerializer(serializers.ModelSerializer):
    plano_nome = serializers.CharField(source='plano.nome', read_only=True, default=None)
    limite_mensal = serializers.SerializerMethodField()
    limite_diario = serializers.SerializerMethodField()
    limite_tamanho_mb = serializers.SerializerMethodField()
    acesso_upscale = serializers.SerializerMethodField()
    is_active_subscriber = serializers.BooleanField(read_only=True)

    class Meta:
        model = UsuarioAssinatura
        fields = [
            'plano_nome', 'limite_mensal', 'limite_diario',
            'limite_tamanho_mb', 'acesso_upscale', 'uso_atual',
            'uso_diario_atual', 'data_inicio', 'data_renovacao',
            'status_assinatura', 'is_active_subscriber',
        ]

    def get_limite_mensal(self, obj):
        return obj.limite_mensal

    def get_limite_diario(self, obj):
        return obj.limite_diario

    def get_limite_tamanho_mb(self, obj):
        return obj.limite_tamanho_mb

    def get_acesso_upscale(self, obj):
        return obj.acesso_upscale


class HistoricoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoPagamento
        fields = [
            'id', 'stripe_invoice_id', 'valor', 'moeda',
            'status', 'data_pagamento', 'data_criacao', 'descricao',
        ]
        read_only_fields = fields
