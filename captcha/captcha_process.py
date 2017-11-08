
from PIL import Image


def preprocess_pixel(image) :
    image_data = image.load()
    
    for width_index in range(image.size[0]) :
        for height_index in range(image.size[1]) :
            image_data[width_index,height_index] &= 0x80
    
def preprocess_captcha(picture_path = 'get_captcha.png') :
    image = Image.open(picture_path)
    image = image.convert('L')
    
    preprocess_pixel(image)
    
    return image



