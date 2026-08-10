import os
from wand.image import Image

def convert_image(input_path, output_path, format='PNG', quality=90):
    """
    Convert image using ImageMagick (via Wand).
    Supports JPEG, JPG, PNG, WEBP, etc.
    """
    try:
        with Image(filename=input_path) as img:
            img.format = format.lower()
            if format.lower() in ['jpeg', 'jpg']:
                img.compression_quality = quality
            img.save(filename=output_path)
        return True
    except Exception as e:
        print(f"Error in convert_image: {e}")
        raise e
