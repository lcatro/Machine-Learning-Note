
import os

from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
from PIL import ImageFont

from captcha_process import *


system_font_dir = 'C:\\Windows\\Fonts\\'


def make_char_set() :
    result = []
    
    for index in range(48,48 + 10) :
        result.append(chr(index))
    
    for index in range(65,65 + 26) :
        result.append(chr(index))
    
    for index in range(97,97 + 26) :
        result.append(chr(index))
    
    return result
    
def make_picture(char,font_name,rotate = 0) :
    image = Image.new('RGB',(16,16),'black')
    
    try :
        font = ImageFont.truetype(system_font_dir + font_name,18)
    except :
        return
    
    draw = ImageDraw.Draw(image)
    
    draw.text((0,-1),char,font = font,fill = 'white')
    
    image = image.rotate(rotate)
    image = image.convert('L')
    image = ImageChops.invert(image)
    
    preprocess_pixel(image)
    
    if ord(char) in range(97,97 + 26) :  #  is little character ..
        image.save('captcha_pic\\' + font_name + '_' + str(rotate) + '__' + char + '.bmp')  #  because Windows no support mix big/little character file name ..
    else :
        image.save('captcha_pic\\' + font_name + '_' + str(rotate)  + '_' + char + '.bmp')
    
    
if __name__ == '__main__' :
    font_list = ['arial.ttf','arialbd.ttf']#,'Candaraz.ttf']
    
    for font_index in font_list :
        for char_index in make_char_set() :
            for rotate_index in range(-25,25,2) :
                make_picture(char_index,font_index,rotate_index)
