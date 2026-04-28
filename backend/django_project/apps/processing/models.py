from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Servico

class UsoServico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_uso = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField(default=True)

class ExecucaoLocal(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')
    progresso = models.IntegerField(default=0)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)

class ArquivoProcessado(models.Model):
    execucao = models.ForeignKey(ExecucaoLocal, on_delete=models.CASCADE, related_name='arquivos')
    arquivo_original = models.FileField(upload_to='uploads/%Y/%m/%d/')
    nome_original = models.CharField(max_length=255)
    tamanho = models.BigIntegerField()

class ResultadoProcessamento(models.Model):
    arquivo_processado = models.OneToOneField(ArquivoProcessado, on_delete=models.CASCADE, related_name='resultado')
    arquivo_final = models.FileField(upload_to='results/%Y/%m/%d/')
    data_conclusao = models.DateTimeField(auto_now_add=True)
