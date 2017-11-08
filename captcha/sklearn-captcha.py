
from os import *
from time import *

from numpy import *

from PIL import Image

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from captcha_process import *


sample_dir = 'captcha_pic'


def image_convert_to_array(image_data,image_width,image_height) :
    pixel_data = []
    
    for width_index in range(image_width) :
        pixel_list_data = []
        
        for height_index in range(image_height) :
            pixel_list_data.append(~image_data[width_index,height_index])
            
        pixel_data += pixel_list_data
    
    return array(pixel_data)

def load_image(path) :
    image = Image.open(path)
    image_data = image.load()
    
    return image_convert_to_array(image_data,image.size[0],image.size[1])

def load_sample() :
    sample_files = listdir(sample_dir)
    data_list = []
    classfy_list = []
    
    for file_index in sample_files :
        file_path = sample_dir + '\\' + file_index
        image_data = load_image(file_path)
        number_class = file_index[file_index.rfind('_') + 1 : file_index.rfind('.')]
        
        data_list.append(image_data)
        classfy_list.append(number_class)
        
    return data_list , classfy_list

def train_model(data_list,classfy_list) :
    svc_model = SVC(gamma = 0.001)
    
    svc_model.fit(data_list,classfy_list)
    
    return svc_model

def try_classfy(train_model,image_data) :
    return train_model.predict(image_data)

def load_captcha(path = 'get_captcha.png',captcha_count = 4) :
    image = preprocess_captcha(path)
    image_width = image.size[0]
    image = image.resize((image_width,32),Image.ANTIALIAS)
    image_data = []
    
    for index in range(captcha_count) :  #  split 4 char
        image_char = image.crop((index * 32,0,(index + 1) * 32,32))
        
        image_data.append(image_convert_to_array(image_char.load(),image_char.size[0],image_char.size[1]))
    
    return image_data

if __name__ == '__main__' :
    start_time = time()
    data_list,classfy_list = load_sample()
    
    print 'Load Data Success'
    
    svc_model = train_model(data_list,classfy_list)
    
    print 'Train Model Success'
    
    image_data = load_captcha()
    
    print 'Load Captche Success'
    print try_classfy(svc_model,image_data)
    print 'Using Time :',time() - start_time
        