import os
from rembg import remove
from PIL import Image
import io

def remove_background(input_path, output_path, use_gpu=False):
    """
    Remove background using rembg.
    Output is always a transparent PNG.
    """
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            
        # rembg.remove automatically handles CPU/GPU if providers are installed
        # In a real environment, we might specify providers=['CUDAExecutionProvider']
        output_data = remove(input_data)
        
        with open(output_path, 'wb') as o:
            o.write(output_data)
            
        return True
    except Exception as e:
        print(f"Error in remove_background: {e}")
        raise e
