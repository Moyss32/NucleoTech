from rest_framework import serializers
from .models import ExecucaoLocal, Arquivo, ArquivoProcessado, ResultadoProcessamento

class ArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arquivo
        fields = ['id', 'nome_original', 'extensao', 'tamanho', 'data_upload']

class ExecucaoLocalSerializer(serializers.ModelSerializer):
    servico_nome = serializers.CharField(source='servico.nome', read_only=True)
    servico_slug = serializers.CharField(source='servico.slug', read_only=True)
    
    class Meta:
        model = ExecucaoLocal
        fields = [
            'task_id', 'servico_nome', 'servico_slug', 'status', 
            'status_detalhado', 'progresso', 'data_inicio', 'data_fim', 
            'tempo_execucao', 'formato_entrada', 'formato_saida'
        ]
