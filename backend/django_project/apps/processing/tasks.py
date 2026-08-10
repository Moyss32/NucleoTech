import os
import sys
import uuid
import time
import mimetypes
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import ExecucaoLocal, Arquivo, ArquivoProcessado, ResultadoProcessamento, UsoServico
from apps.subscriptions.models import UsuarioAssinatura


def _get_tools():
    """Lazy import of processing tools to avoid import errors at startup."""
    tools_dir = os.path.join(settings.BASE_DIR, '..')
    if tools_dir not in sys.path:
        sys.path.append(tools_dir)
    from tools.image_tools.background_removal import remove_background
    from tools.image_tools.upscale import upscale_image
    from tools.image_tools.image_convert import convert_image
    from tools.image_tools.thumbnail import generate_thumbnail
    from tools.audio_tools.audio_convert import convert_audio
    return {
        'remove_background': remove_background,
        'upscale_image': upscale_image,
        'convert_image': convert_image,
        'generate_thumbnail': generate_thumbnail,
        'convert_audio': convert_audio,
    }


def _guess_mime_type(filename: str) -> str:
    """Returns a proper MIME type for the given filename."""
    mime, _ = mimetypes.guess_type(filename)
    return mime or 'application/octet-stream'


@shared_task(bind=True)
def run_processing_task(self, task_id, tool_slug, input_file_id, output_format=None):
    start_time = time.time()
    try:
        execucao = ExecucaoLocal.objects.get(task_id=task_id)
        execucao.status = 'processing'
        execucao.status_detalhado = 'Iniciando processamento...'
        execucao.progresso = 10
        execucao.save()

        arquivo_input = Arquivo.objects.get(id=input_file_id)
        input_path = arquivo_input.caminho_armazenamento.path

        # Prepare output
        output_ext = output_format if output_format else arquivo_input.extensao.lstrip('.')
        output_filename = f"{uuid.uuid4()}.{output_ext}"
        output_dir = os.path.join(settings.MEDIA_ROOT, 'results', timezone.now().strftime('%Y/%m/%d'))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)

        execucao.status_detalhado = f"Executando ferramenta: {tool_slug}"
        execucao.progresso = 30
        execucao.save()

        tools = _get_tools()
        if tool_slug == 'remove-bg':
            tools['remove_background'](input_path, output_path)
        elif tool_slug == 'upscale':
            scale = execucao.parametros_processamento.get('scale', 2) if execucao.parametros_processamento else 2
            tools['upscale_image'](input_path, output_path, scale=scale)
        elif tool_slug == 'convert-image':
            tools['convert_image'](input_path, output_path, format=output_ext.upper())
        elif tool_slug == 'thumbnail':
            tools['generate_thumbnail'](input_path, output_path)
        elif tool_slug == 'convert-audio':
            tools['convert_audio'](input_path, output_path)
        else:
            raise ValueError(f"Ferramenta desconhecida: {tool_slug}")

        execucao.progresso = 90
        execucao.status_detalhado = "Finalizando e salvando resultados..."
        execucao.save()

        # Get relative path for FileField storage
        rel_path = os.path.relpath(output_path, settings.MEDIA_ROOT)

        # Determine proper mime type based on output file name
        output_mime = _guess_mime_type(output_filename)

        arquivo_output = Arquivo.objects.create(
            usuario=execucao.usuario,
            nome_original=f"processed_{arquivo_input.nome_original.rsplit('.', 1)[0]}.{output_ext}",
            nome_interno_unico=output_filename,
            extensao=f".{output_ext}",
            mime_type=output_mime,
            tamanho=os.path.getsize(output_path),
            caminho_armazenamento=rel_path,
        )

        # Update processing models
        arquivo_proc = ArquivoProcessado.objects.get(execucao=execucao)
        ResultadoProcessamento.objects.create(
            arquivo_processado=arquivo_proc,
            arquivo_final_obj=arquivo_output,
            arquivo_final=rel_path,  # Compatibility field
        )

        end_time = time.time()
        execucao.progresso = 100
        execucao.status = 'completed'
        execucao.status_detalhado = "Processamento concluído com sucesso."
        execucao.data_fim = timezone.now()
        execucao.tempo_execucao = timezone.timedelta(seconds=int(end_time - start_time))
        execucao.save()

        # Update usage counters
        try:
            ua = UsuarioAssinatura.objects.get(usuario=execucao.usuario)
            ua.uso_atual += 1
            ua.uso_diario_atual += 1
            ua.save(update_fields=['uso_atual', 'uso_diario_atual'])
        except UsuarioAssinatura.DoesNotExist:
            pass

        UsoServico.objects.create(
            usuario=execucao.usuario,
            servico=execucao.servico,
            sucesso=True,
        )

        return {'status': 'success', 'task_id': task_id}

    except Exception as e:
        error_msg = str(e)
        import traceback
        tb = traceback.format_exc()
        print(f"Error processing task {task_id}: {error_msg}\n{tb}")
        try:
            execucao = ExecucaoLocal.objects.get(task_id=task_id)
            execucao.status = 'failed'
            execucao.status_detalhado = "Erro durante o processamento."
            execucao.logs_de_erro = f"{error_msg}\n\n{tb}"
            execucao.data_fim = timezone.now()
            execucao.save()

            UsoServico.objects.create(
                usuario=execucao.usuario,
                servico=execucao.servico,
                sucesso=False,
            )
        except Exception:
            pass
        return {'status': 'error', 'message': error_msg}
