
import os

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

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
    
def make_picture(char,location,font_name) :
    image = Image.new('RGB',(32,32),'white')
    
    try :
        font = ImageFont.truetype(system_font_dir + font_name,32)
    except :
        try :
            font = ImageFont.truetype(system_font_dir + font_name,24)
        except :
            return
    
    draw = ImageDraw.Draw(image)

    draw.text(location,char,font = font,fill = 'black')

    image = image.convert('L')

    preprocess_pixel(image)

    image.save('captcha_pic\\' + font_name + '_' + char + '.bmp')
    
    
if __name__ == '__main__' :
    print make_char_set()
    
    '''
    font_list = os.listdir(system_font_dir)

    for font_index in font_list :
        for char_index in make_char_set() :
            make_picture(char_index,(5,0),font_index)
    '''
