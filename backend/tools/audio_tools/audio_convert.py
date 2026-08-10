import subprocess
import os
import json

def get_audio_metadata(input_path):
    """Extract metadata using ffprobe."""
    try:
        cmd = [
            'ffprobe', 
            '-v', 'quiet', 
            '-print_format', 'json', 
            '-show_format', 
            '-show_streams', 
            input_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {}

def convert_audio(input_path, output_path, codec=None, bitrate=None):
    """
    Convert audio using FFmpeg.
    Supports MP3, WAV, AAC, OGG, OPUS, FLAC.
    """
    try:
        cmd = ['ffmpeg', '-i', input_path, '-y']
        
        if codec:
            cmd.extend(['-c:a', codec])
        
        if bitrate:
            cmd.extend(['-b:a', bitrate])
            
        cmd.append(output_path)
        
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise Exception(f"FFmpeg failed: {e.stderr.decode()}")
    except Exception as e:
        print(f"Error in convert_audio: {e}")
        raise e
