from django.contrib import admin
from .models import Arquivo, ExecucaoLocal, ArquivoProcessado, ResultadoProcessamento, UsoServico


@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_original', 'extensao', 'mime_type', 'tamanho', 'usuario', 'data_upload']
    list_filter = ['extensao', 'data_upload']
    search_fields = ['nome_original', 'usuario__username', 'nome_interno_unico']
    readonly_fields = ['id', 'data_upload', 'hash_arquivo']
    raw_id_fields = ['usuario']


@admin.register(ExecucaoLocal)
class ExecucaoLocalAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'usuario', 'servico', 'status', 'progresso', 'data_inicio', 'data_fim']
    list_filter = ['status', 'servico']
    search_fields = ['task_id', 'usuario__username']
    readonly_fields = ['task_id', 'data_inicio', 'data_fim', 'tempo_execucao']
    raw_id_fields = ['usuario', 'servico']


@admin.register(UsoServico)
class UsoServicoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'servico', 'data_uso', 'sucesso']
    list_filter = ['sucesso', 'servico']
    search_fields = ['usuario__username']
    raw_id_fields = ['usuario', 'servico']
