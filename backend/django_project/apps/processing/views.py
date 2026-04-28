import uuid
import os
import threading
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ExecucaoLocal, ArquivoProcessado, ResultadoProcessamento, UsoServico
from .serializers import ExecucaoLocalSerializer
from apps.services.models import Servico
from apps.subscriptions.models import UsuarioAssinatura

# Import tools
import sys
sys.path.append(os.path.join(settings.BASE_DIR, '..'))
from tools.image_tools.background_removal import remove_background
from tools.image_tools.upscale import upscale_image
from tools.image_tools.image_convert import convert_image
from tools.image_tools.thumbnail import generate_thumbnail
from tools.audio_tools.audio_convert import convert_audio

def run_processing_task(task_id, tool_slug, input_path, output_path):
    try:
        execucao = ExecucaoLocal.objects.get(task_id=task_id)
        execucao.status = 'processing'
        execucao.progresso = 10
        execucao.save()

        if tool_slug == 'remove-bg':
            remove_background(input_path, output_path)
        elif tool_slug == 'upscale':
            upscale_image(input_path, output_path)
        elif tool_slug == 'convert-image':
            convert_image(input_path, output_path)
        elif tool_slug == 'thumbnail':
            generate_thumbnail(input_path, output_path)
        elif tool_slug == 'convert-audio':
            convert_audio(input_path, output_path)
        
        execucao.progresso = 100
        execucao.status = 'completed'
        execucao.save()
        
        # Save result
        arquivo_proc = execucao.arquivos.first()
        ResultadoProcessamento.objects.create(
            arquivo_processado=arquivo_proc,
            arquivo_final=output_path.replace(str(settings.BASE_DIR) + '/', '')
        )
        
        # Update usage
        ua = UsuarioAssinatura.objects.get(usuario=execucao.usuario)
        ua.uso_atual += 1
        ua.save()
        
        UsoServico.objects.create(
            usuario=execucao.usuario,
            servico=execucao.servico,
            sucesso=True
        )

    except Exception as e:
        print(f"Error processing task {task_id}: {e}")
        execucao = ExecucaoLocal.objects.get(task_id=task_id)
        execucao.status = 'failed'
        execucao.save()

class ProcessFileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        file_obj = request.FILES.get('file')
        tool_slug = request.data.get('tool')
        
        if not file_obj or not tool_slug:
            return Response({'error': 'File and tool are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            servico = Servico.objects.get(slug=tool_slug)
        except Servico.DoesNotExist:
            return Response({'error': 'Invalid tool'}, status=status.HTTP_400_BAD_REQUEST)

        # Check subscription limit
        ua, _ = UsuarioAssinatura.objects.get_or_create(usuario=request.user)
        if ua.plano and ua.uso_atual >= ua.plano.limite_mensal:
            return Response({'error': 'Monthly limit reached'}, status=status.HTTP_403_FORBIDDEN)

        task_id = str(uuid.uuid4())
        execucao = ExecucaoLocal.objects.create(
            task_id=task_id,
            usuario=request.user,
            servico=servico,
            status='pending'
        )
        
        arquivo_proc = ArquivoProcessado.objects.create(
            execucao=execucao,
            arquivo_original=file_obj,
            nome_original=file_obj.name,
            tamanho=file_obj.size
        )
        
        # Prepare paths
        input_path = arquivo_proc.arquivo_original.path
        output_filename = f"processed_{task_id}_{file_obj.name}"
        output_dir = os.path.join(settings.MEDIA_ROOT, 'results')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        
        # Run in background thread (simple alternative to Celery for local dev)
        thread = threading.Thread(target=run_processing_task, args=(task_id, tool_slug, input_path, output_path))
        thread.start()
        
        return Response({
            'task_id': task_id,
            'status': 'pending'
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
            if hasattr(arquivo_proc, 'resultado'):
                download_url = request.build_absolute_uri(arquivo_proc.resultado.arquivo_final.url)
        
        return Response({
            'status': execucao.status,
            'progress': execucao.progresso,
            'download_url': download_url
        })

class HistoryListView(generics.ListAPIView):
    serializer_class = ExecucaoLocalSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ExecucaoLocal.objects.filter(usuario=self.request.user).order_by('-data_inicio')
