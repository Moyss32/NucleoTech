from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Servico


class Assinatura(models.Model):
    nome = models.CharField(max_length=100)
    limite_mensal = models.IntegerField()
    limite_diario = models.IntegerField(default=5)
    limite_tamanho_arquivo_mb = models.IntegerField(default=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    prioridade_fila = models.IntegerField(default=0)
    acesso_upscale = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)

    # Stripe integration fields
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_product_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Plano de Assinatura'
        verbose_name_plural = 'Planos de Assinatura'

    def __str__(self):
        return self.nome


class UsuarioAssinatura(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('canceled', 'Cancelado'),
        ('past_due', 'Pagamento Atrasado'),
        ('trialing', 'Em Teste'),
        ('unpaid', 'Não Pago'),
        ('incomplete', 'Incompleto'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assinatura_perfil')
    plano = models.ForeignKey(Assinatura, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateTimeField(auto_now_add=True)
    uso_atual = models.IntegerField(default=0)
    uso_diario_atual = models.IntegerField(default=0)
    data_ultimo_reset_diario = models.DateField(auto_now_add=True)
    data_renovacao = models.DateTimeField(null=True, blank=True)

    # Stripe integration fields
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    status_assinatura = models.CharField(max_length=50, choices=STATUS_CHOICES, default='inactive')

    class Meta:
        verbose_name = 'Assinatura de Usuário'
        verbose_name_plural = 'Assinaturas de Usuários'

    def __str__(self):
        return f"{self.usuario.username} - {self.plano.nome if self.plano else 'Sem Plano'}"

    @property
    def is_active_subscriber(self):
        """Returns True if the user has an active paid subscription."""
        return self.status_assinatura in ('active', 'trialing') and self.plano is not None

    @property
    def limite_mensal(self):
        if self.plano:
            return self.plano.limite_mensal
        return 5  # Free tier default

    @property
    def limite_diario(self):
        if self.plano:
            return self.plano.limite_diario
        return 2  # Free tier default

    @property
    def limite_tamanho_mb(self):
        if self.plano:
            return self.plano.limite_tamanho_arquivo_mb
        return 10  # Free tier default (10MB)

    @property
    def acesso_upscale(self):
        if self.plano:
            return self.plano.acesso_upscale
        return False


class HistoricoPagamento(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Pago'),
        ('failed', 'Falhou'),
        ('refunded', 'Reembolsado'),
        ('pending', 'Pendente'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_pagamentos')
    assinatura_usuario = models.ForeignKey(
        UsuarioAssinatura, on_delete=models.CASCADE, related_name='pagamentos', null=True
    )
    stripe_invoice_id = models.CharField(max_length=255, unique=True)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    moeda = models.CharField(max_length=10, default='brl')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    data_pagamento = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Histórico de Pagamento'
        verbose_name_plural = 'Histórico de Pagamentos'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.usuario.username} - {self.valor} {self.moeda.upper()} ({self.status})"
