import rembg
from PIL import Image
import io

def remove_background(input_path, output_path):
    with open(input_path, 'rb') as i:
        input_data = i.read()
        output_data = rembg.remove(input_data)
        with open(output_path, 'wb') as o:
            o.write(output_data)
    return output_path
