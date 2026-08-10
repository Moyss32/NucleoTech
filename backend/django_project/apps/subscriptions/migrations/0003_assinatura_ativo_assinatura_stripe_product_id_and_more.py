# Generated migration for new subscription fields

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_assinatura_acesso_upscale_assinatura_limite_diario_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Assinatura: new fields
        migrations.AddField(
            model_name='assinatura',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='assinatura',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),

        # UsuarioAssinatura: new fields
        migrations.AddField(
            model_name='usuarioassinatura',
            name='data_renovacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usuarioassinatura',
            name='status_assinatura',
            field=models.CharField(
                choices=[
                    ('active', 'Ativo'),
                    ('inactive', 'Inativo'),
                    ('canceled', 'Cancelado'),
                    ('past_due', 'Pagamento Atrasado'),
                    ('trialing', 'Em Teste'),
                    ('unpaid', 'Não Pago'),
                    ('incomplete', 'Incompleto'),
                ],
                default='inactive',
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name='usuarioassinatura',
            name='plano',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='subscriptions.assinatura',
            ),
        ),

        # Add db_index to stripe fields
        migrations.AlterField(
            model_name='usuarioassinatura',
            name='stripe_customer_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usuarioassinatura',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),

        # HistoricoPagamento: new model
        migrations.CreateModel(
            name='HistoricoPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_invoice_id', models.CharField(max_length=255, unique=True)),
                ('stripe_payment_intent_id', models.CharField(blank=True, max_length=255, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('moeda', models.CharField(default='brl', max_length=10)),
                ('status', models.CharField(
                    choices=[
                        ('paid', 'Pago'),
                        ('failed', 'Falhou'),
                        ('refunded', 'Reembolsado'),
                        ('pending', 'Pendente'),
                    ],
                    default='pending',
                    max_length=50,
                )),
                ('data_pagamento', models.DateTimeField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='historico_pagamentos',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('assinatura_usuario', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pagamentos',
                    to='subscriptions.usuarioassinatura',
                )),
            ],
            options={
                'verbose_name': 'Histórico de Pagamento',
                'verbose_name_plural': 'Histórico de Pagamentos',
                'ordering': ['-data_criacao'],
            },
        ),
    ]
