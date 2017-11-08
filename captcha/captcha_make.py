
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
    
    if ord(char) in range(97,97 + 26) :  #  is little character ..
        image.save('captcha_pic\\' + font_name + '__' + char + '.bmp')  #  because Windows no support mix big/little character file name ..
    else :
        image.save('captcha_pic\\' + font_name + '_' + char + '.bmp')
    
    
if __name__ == '__main__' :
    font_list = ['ahronbd','angsaub.ttf','angsauz.ttf','aparaj.ttf','aparajbi.ttf','arial.ttf','arialbd.ttf','browaz.ttf','Candaraz.ttf','lvnm.ttf']#os.listdir(system_font_dir)
    
    for font_index in font_list :
        #if not font_index.endswith('.ttf') :
        #    continue
            
        for char_index in make_char_set() :
            make_picture(char_index,(5,0),font_index)
