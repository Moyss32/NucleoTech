from PIL import Image

def upscale_image(input_path, output_path, scale=2):
    img = Image.open(input_path)
    width, height = img.size
    new_size = (width * scale, height * scale)
    # Using Lanczos for high-quality downsampling/upsampling
    res = img.resize(new_size, Image.LANCZOS)
    res.save(output_path)
    return output_path
