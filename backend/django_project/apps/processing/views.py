import uuid
import os
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ExecucaoLocal, Arquivo, ArquivoProcessado, ResultadoProcessamento, UsoServico
from .serializers import ExecucaoLocalSerializer
from apps.services.models import Servico
from apps.subscriptions.models import UsuarioAssinatura
from .tasks import run_processing_task

class ProcessFileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        file_obj = request.FILES.get('file')
        tool_slug = request.data.get('tool')
        output_format = request.data.get('output_format')
        
        if not file_obj or not tool_slug:
            return Response({'error': 'File and tool are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            servico = Servico.objects.get(slug=tool_slug)
        except Servico.DoesNotExist:
            return Response({'error': 'Invalid tool'}, status=status.HTTP_400_BAD_REQUEST)

        # Check subscription and limits
        ua, _ = UsuarioAssinatura.objects.get_or_create(usuario=request.user)
        plano = ua.plano
        
        if plano:
            # Check monthly limit
            if ua.uso_atual >= plano.limite_mensal:
                return Response({'error': 'Monthly limit reached'}, status=status.HTTP_403_FORBIDDEN)
            
            # Check daily limit
            if ua.data_ultimo_reset_diario != timezone.now().date():
                ua.uso_diario_atual = 0
                ua.data_ultimo_reset_diario = timezone.now().date()
                ua.save()
            
            if ua.uso_diario_atual >= plano.limite_diario:
                return Response({'error': 'Daily limit reached'}, status=status.HTTP_403_FORBIDDEN)
            
            # Check file size limit
            if file_obj.size > (plano.limite_tamanho_arquivo_mb * 1024 * 1024):
                return Response({'error': f'File size exceeds limit for your plan ({plano.limite_tamanho_arquivo_mb}MB)'}, status=status.HTTP_403_FORBIDDEN)
            
            # Check upscale access
            if tool_slug == 'upscale' and not plano.acesso_upscale:
                return Response({'error': 'Upscale service is not available in your plan'}, status=status.HTTP_403_FORBIDDEN)

        # 1. Create Arquivo object
        ext = os.path.splitext(file_obj.name)[1]
        nome_interno = f"{uuid.uuid4()}{ext}"
        
        arquivo = Arquivo.objects.create(
            usuario=request.user,
            nome_original=file_obj.name,
            nome_interno_unico=nome_interno,
            extensao=ext,
            mime_type=file_obj.content_type,
            tamanho=file_obj.size,
            caminho_armazenamento=file_obj
        )
        
        # 2. Create ExecucaoLocal
        task_id = str(uuid.uuid4())
        execucao = ExecucaoLocal.objects.create(
            task_id=task_id,
            usuario=request.user,
            servico=servico,
            status='queued',
            formato_entrada=ext,
            formato_saida=output_format if output_format else ext,
            parametros_processamento=request.data.get('params', {})
        )
        
        # 3. Create ArquivoProcessado link
        ArquivoProcessado.objects.create(
            execucao=execucao,
            arquivo_referencia=arquivo,
            nome_original=file_obj.name, # Compatibility
            tamanho=file_obj.size # Compatibility
        )
        
        # 4. Dispatch to Celery
        run_processing_task.delay(
            task_id=task_id,
            tool_slug=tool_slug,
            input_file_id=str(arquivo.id),
            output_format=output_format
        )
        
        return Response({
            'task_id': task_id,
            'status': 'queued'
        })

class ProcessStatusView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, task_id):
        try:
            execucao = ExecucaoLocal.objects.get(task_id=task_id, usuario=request.user)
        except ExecucaoLocal.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            
        download_url = None
        if execucao.status == 'completed':
            arquivo_proc = execucao.arquivos.first()
            if hasattr(arquivo_proc, 'resultado') and arquivo_proc.resultado.arquivo_final_obj:
                # Use secure download URL instead of direct link
                download_url = request.build_absolute_uri(f"/api/files/{arquivo_proc.resultado.arquivo_final_obj.id}/download/")
        
        return Response({
            'status': execucao.status,
            'status_detalhado': execucao.status_detalhado,
            'progress': execucao.progresso,
            'download_url': download_url,
            'data_inicio': execucao.data_inicio,
            'data_fim': execucao.data_fim,
            'tempo_execucao': execucao.tempo_execucao.total_seconds() if execucao.tempo_execucao else None
        })

class HistoryListView(generics.ListAPIView):
    serializer_class = ExecucaoLocalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ExecucaoLocal.objects.filter(usuario=self.request.user).order_by('-data_inicio')
