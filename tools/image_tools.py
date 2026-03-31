import os
from PIL import Image
from rembg import remove
import io

def convert_image(input_path, output_path, target_format):
    """Converte imagem para PNG, JPG ou WebP."""
    with Image.open(input_path) as img:
        if target_format.upper() == 'JPG' or target_format.upper() == 'JPEG':
            img = img.convert('RGB')
        img.save(output_path, target_format.upper())
    return output_path

def remove_background(input_path, output_path):
    """Remove o fundo da imagem usando rembg."""
    with open(input_path, 'rb') as i:
        input_data = i.read()
        output_data = remove(input_data)
        with open(output_path, 'wb') as o:
            o.write(output_data)
    return output_path

def upscale_image(input_path, output_path, factor=1.5):
    """Aumenta a resolução da imagem (Upscale simples via Lanczos)."""
    with Image.open(input_path) as img:
        width, height = img.size
        new_size = (int(width * factor), int(height * factor))
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        img_resized.save(output_path)
    return output_path

def generate_thumbnail(input_path, output_path, size=(200, 200)):
    """Gera uma thumbnail da imagem."""
    with Image.open(input_path) as img:
        img.thumbnail(size)
        img.save(output_path)
    return output_path
