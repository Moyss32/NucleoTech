from django.contrib import admin
from .models import Assinatura, UsuarioAssinatura, HistoricoPagamento


@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'limite_mensal', 'limite_diario', 'acesso_upscale', 'ativo', 'stripe_price_id']
    list_filter = ['ativo', 'acesso_upscale']
    search_fields = ['nome', 'stripe_price_id', 'stripe_product_id']
    list_editable = ['ativo']


@admin.register(UsuarioAssinatura)
class UsuarioAssinaturaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'plano', 'status_assinatura', 'uso_atual', 'uso_diario_atual', 'data_renovacao']
    list_filter = ['status_assinatura', 'plano']
    search_fields = ['usuario__username', 'usuario__email', 'stripe_customer_id', 'stripe_subscription_id']
    readonly_fields = ['stripe_customer_id', 'stripe_subscription_id', 'data_inicio']
    raw_id_fields = ['usuario', 'plano']


@admin.register(HistoricoPagamento)
class HistoricoPagamentoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'valor', 'moeda', 'status', 'data_pagamento', 'stripe_invoice_id']
    list_filter = ['status', 'moeda']
    search_fields = ['usuario__username', 'stripe_invoice_id', 'stripe_payment_intent_id']
    readonly_fields = ['stripe_invoice_id', 'stripe_payment_intent_id', 'data_criacao']
    raw_id_fields = ['usuario', 'assinatura_usuario']
