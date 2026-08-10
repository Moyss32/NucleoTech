import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Servico

class Arquivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arquivos_enviados')
    nome_original = models.CharField(max_length=255)
    nome_interno_unico = models.CharField(max_length=255, unique=True)
    extensao = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=100)
    tamanho = models.BigIntegerField()
    hash_arquivo = models.CharField(max_length=64, null=True, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    caminho_armazenamento = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.nome_original

class UsoServico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_uso = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField(default=True)

class ExecucaoLocal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('queued', 'Na Fila'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('cancelled', 'Cancelado'),
    ]

    task_id = models.CharField(max_length=255, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    status_detalhado = models.CharField(max_length=255, null=True, blank=True)
    progresso = models.IntegerField(default=0)
    logs_de_erro = models.TextField(null=True, blank=True)
    tempo_execucao = models.DurationField(null=True, blank=True)
    formato_entrada = models.CharField(max_length=50, null=True, blank=True)
    formato_saida = models.CharField(max_length=50, null=True, blank=True)
    parametros_processamento = models.JSONField(null=True, blank=True)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.servico.nome} - {self.task_id} ({self.status})"

class ArquivoProcessado(models.Model):
    execucao = models.ForeignKey(ExecucaoLocal, on_delete=models.CASCADE, related_name='arquivos')
    arquivo_referencia = models.ForeignKey(Arquivo, on_delete=models.CASCADE, related_name='processamentos', null=True)
    # Mantendo os campos antigos para compatibilidade durante a migração, mas serão depreciados
    arquivo_original = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    nome_original = models.CharField(max_length=255, null=True, blank=True)
    tamanho = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Arquivo de {self.execucao.task_id}"

class ResultadoProcessamento(models.Model):
    arquivo_processado = models.OneToOneField(ArquivoProcessado, on_delete=models.CASCADE, related_name='resultado')
    arquivo_final_obj = models.ForeignKey(Arquivo, on_delete=models.CASCADE, related_name='resultados', null=True)
    # Mantendo para compatibilidade
    arquivo_final = models.FileField(upload_to='results/%Y/%m/%d/', null=True, blank=True)
    data_conclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resultado de {self.arquivo_processado.execucao.task_id}"
