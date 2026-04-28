from PIL import Image

def convert_image(input_path, output_path, format='PNG'):
    img = Image.open(input_path)
    img.save(output_path, format=format)
    return output_path
