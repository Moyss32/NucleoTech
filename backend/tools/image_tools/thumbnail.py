from PIL import Image

def generate_thumbnail(input_path, output_path, size=(128, 128)):
    img = Image.open(input_path)
    img.thumbnail(size)
    img.save(output_path)
    return output_path
