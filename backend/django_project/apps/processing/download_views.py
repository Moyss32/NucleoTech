import os
import logging
import mimetypes
from django.http import StreamingHttpResponse, HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Arquivo

logger = logging.getLogger(__name__)

# Streaming chunk size: 8 KB
CHUNK_SIZE = 8 * 1024


def _file_iterator(file_path, chunk_size=CHUNK_SIZE):
    """Generator that yields file content in chunks for streaming."""
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


class SecureDownloadView(APIView):
    """
    GET /api/files/<uuid:file_id>/download/

    Secure, streaming file download endpoint.
    - Requires authentication.
    - Validates ownership: only the file owner can download.
    - Checks physical file existence.
    - Streams large files without loading into memory.
    - Logs invalid access attempts.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, file_id):
        # 1. Fetch file record from DB
        try:
            arquivo = Arquivo.objects.get(id=file_id)
        except Arquivo.DoesNotExist:
            logger.warning(
                f"Download attempt for non-existent file {file_id} by user {request.user.id} "
                f"(IP: {_get_client_ip(request)})"
            )
            return Response(
                {'error': 'Arquivo não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Validate ownership
        if arquivo.usuario_id != request.user.id:
            logger.warning(
                f"Unauthorized download attempt: user {request.user.id} tried to access "
                f"file {file_id} owned by user {arquivo.usuario_id} "
                f"(IP: {_get_client_ip(request)})"
            )
            return Response(
                {'error': 'Você não tem permissão para baixar este arquivo.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Validate physical file existence
        file_path = arquivo.caminho_armazenamento.path
        if not os.path.exists(file_path):
            logger.error(
                f"Physical file missing for Arquivo {file_id} at path: {file_path}"
            )
            return Response(
                {'error': 'Arquivo físico não encontrado no servidor.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 4. Determine correct Content-Type
        content_type = arquivo.mime_type
        if not content_type or content_type in ('application/octet-stream', 'application/'):
            # Try to guess from extension
            guessed_type, _ = mimetypes.guess_type(arquivo.nome_original)
            content_type = guessed_type or 'application/octet-stream'

        # 5. Build safe filename for Content-Disposition
        safe_filename = arquivo.nome_original.encode('ascii', 'replace').decode('ascii')
        # RFC 5987 encoding for unicode filenames
        encoded_filename = arquivo.nome_original.encode('utf-8').decode('latin-1', errors='replace')

        # 6. Stream the file response
        file_size = os.path.getsize(file_path)
        response = StreamingHttpResponse(
            _file_iterator(file_path),
            content_type=content_type,
        )
        response['Content-Length'] = file_size
        response['Content-Disposition'] = (
            f"attachment; filename=\"{safe_filename}\"; "
            f"filename*=UTF-8''{arquivo.nome_original}"
        )
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['Cache-Control'] = 'private, no-cache'

        logger.info(
            f"File {file_id} downloaded by user {request.user.id} "
            f"({file_size} bytes, IP: {_get_client_ip(request)})"
        )
        return response


def _get_client_ip(request):
    """Extracts real client IP, respecting X-Forwarded-For when behind a proxy."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')
