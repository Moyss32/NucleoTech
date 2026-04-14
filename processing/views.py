import os
import time
from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Arquivo_Processado, Resultado_Processamento, Uso_Servico, Execucao_Local
from services.models import Service
from tools.image_tools import convert_image, remove_background, upscale_image, generate_thumbnail
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class ImageProcessingView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "Nenhum arquivo enviado"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Registrar o arquivo enviado
        arquivo = Arquivo_Processado.objects.create(
            user=request.user,
            original_filename=file_obj.name,
            stored_filename=file_obj.name, # Simplificado para o exemplo
            file_type=file_obj.content_type,
            file_size=file_obj.size
        )

        # Salvar o arquivo localmente para processamento
        path = default_storage.save(f'uploads/{file_obj.name}', ContentFile(file_obj.read()))
        full_input_path = os.path.join(settings.MEDIA_ROOT, path)
        
        # 2. Identificar o serviço
        service_name_map = {
            'convert': 'Conversão de Imagem',
            'remove_bg': 'Remoção de Fundo',
            'upscale': 'Upscale de Imagem',
            'thumbnail': 'Gerador de Thumbnails'
        }
        service_name = service_name_map.get(action)
        service, _ = Service.objects.get_or_create(name=service_name)

        # 3. Iniciar execução local
        execucao = Execucao_Local.objects.create(
            user=request.user,
            service=service,
            status='Processando'
        )

        start_time = time.time()
        output_filename = f"processed_{action}_{file_obj.name}"
        full_output_path = os.path.join(settings.MEDIA_ROOT, 'results', output_filename)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        try:
            # 4. Executar a ferramenta
            if action == 'convert':
                target_format = request.data.get('format', 'PNG')
                convert_image(full_input_path, full_output_path, target_format)
            elif action == 'remove_bg':
                remove_background(full_input_path, full_output_path)
            elif action == 'upscale':
                upscale_image(full_input_path, full_output_path)
            elif action == 'thumbnail':
                generate_thumbnail(full_input_path, full_output_path)
            else:
                return Response({"error": "Ação inválida"}, status=status.HTTP_400_BAD_REQUEST)

            # 5. Registrar resultado
            Resultado_Processamento.objects.create(
                processed_file=arquivo,
                service_used=service,
                result_filename=output_filename,
                result_file_type='image/png', # Simplificado
                result_file_size=os.path.getsize(full_output_path)
            )

            # 6. Atualizar execução e uso
            execucao.status = 'Concluído'
            execucao.end_time = None # Simplificado
            execucao.save()

            Uso_Servico.objects.create(
                user=request.user,
                service=service,
                cost=service.price_per_use or 0
            )

            return Response({
                "message": "Processamento concluído",
                "result_url": f"{settings.MEDIA_URL}results/{output_filename}"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            execucao.status = 'Erro'
            execucao.details = str(e)
            execucao.save()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
