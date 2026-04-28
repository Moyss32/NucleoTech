from rest_framework import serializers
from .models import ExecucaoLocal, ArquivoProcessado, ResultadoProcessamento, UsoServico

class ExecucaoLocalSerializer(serializers.ModelSerializer):
    servico_nome = serializers.ReadOnlyField(source='servico.nome')
    
    class Meta:
        model = ExecucaoLocal
        fields = ('task_id', 'servico_nome', 'status', 'progresso', 'data_inicio', 'data_fim')
