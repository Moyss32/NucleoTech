import os
from pydub import AudioSegment

def convert_audio(input_path, output_path, target_format):
    """Converte áudio entre WAV e MP3."""
    # Determinar o formato de entrada a partir da extensão
    input_format = os.path.splitext(input_path)[1][1:].lower()
    
    # Carregar o áudio
    audio = AudioSegment.from_file(input_path, format=input_format)
    
    # Exportar no formato de destino
    audio.export(output_path, format=target_format.lower())
    return output_path
