import subprocess

def convert_audio(input_path, output_path):
    # Using ffmpeg via subprocess as requested
    command = ['ffmpeg', '-i', input_path, output_path, '-y']
    subprocess.run(command, check=True)
    return output_path
