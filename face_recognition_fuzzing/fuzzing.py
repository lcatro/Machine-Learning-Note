
import random

from numpy import array
from PIL import Image
from PIL import ImageDraw

import face_recognition


def load_image_encoding(file_path) :
    image = face_recognition.load_image_file(file_path)
    image_encoding = face_recognition.face_encodings(image)[0]
    
    return image_encoding

def get_face_location(file_path) :
    image = face_recognition.load_image_file(file_path)
    face_location = face_recognition.face_locations(image)[0]
    
    return face_location

def fuzzing(source_image_path = 'obama/obama.jpg',fuzzing_image_path = 'ponyma/ponyma.png',target_compare_rate = 0.4) :
    source_face_data = load_image_encoding(source_image_path)
    image = Image.open(fuzzing_image_path)
    draw = ImageDraw.Draw(image)
    last_best_compare_rate = 1
    face_location = get_face_location(fuzzing_image_path)
    random_fuzzing_location_top = face_location[0]
    random_fuzzing_location_bottom = face_location[2]
    random_fuzzing_location_left = face_location[3]
    random_fuzzing_location_right = face_location[1]
    
    while True :
        random_pixel_data = (random.randint(0,255),
                             random.randint(0,255),
                             random.randint(0,255))
        random_location = (random.randint(random_fuzzing_location_left,random_fuzzing_location_right),
                           random.randint(random_fuzzing_location_top,random_fuzzing_location_bottom))
        last_pixel_data = image.getpixel(random_location)
        
        draw.point(random_location,random_pixel_data)
        
        fuzzing_face_image = image.convert('RGB')
        fuzzing_face_array = array(fuzzing_face_image)
        fuzzing_face_data = face_recognition.face_encodings(fuzzing_face_array)[0]
        compare_rate = face_recognition.face_distance([source_face_data],fuzzing_face_data)
        
        print 'Compare Rate =',compare_rate,' Random Location =',random_location,' Random Pixel Data =',random_pixel_data
        
        del fuzzing_face_image  #  for memory-leak ..
        del fuzzing_face_array
        del fuzzing_face_data
        
        if compare_rate < target_compare_rate :
            break
        
        if compare_rate < last_best_compare_rate :
            last_best_compare_rate = compare_rate
            
            print 'New Study Rate:' ,last_best_compare_rate
        else :
            draw.point(random_location,last_pixel_data)
            
    image.save(fuzzing_image_path + '_bypass_check.jpg')


obama_image = face_recognition.load_image_file('obama/obama.jpg')
obama1_image = face_recognition.load_image_file('obama/obama2.jpg')
ponyma_image = face_recognition.load_image_file('ponyma/ponyma.png')
ponyma1_image = face_recognition.load_image_file('ponyma/ponyma.png_bypass_check.jpg')

obama_encoding = face_recognition.face_encodings(obama_image)[0]
obama1_encoding = face_recognition.face_encodings(obama1_image)[0]
ponyma_image = face_recognition.face_encodings(ponyma_image)[0]
ponyma1_image = face_recognition.face_encodings(ponyma1_image)[0]

print 'Obama Test:'
print face_recognition.compare_faces([obama_encoding], obama1_encoding),\
      face_recognition.face_distance([obama_encoding], obama1_encoding)
print 'PonyMa test:'
print face_recognition.compare_faces([obama_encoding], ponyma_image),\
      face_recognition.face_distance([obama_encoding], ponyma_image)
print 'PonyMa Bypass test:'
print face_recognition.compare_faces([obama_encoding], ponyma1_image),\
      face_recognition.face_distance([obama_encoding], ponyma1_image)


#print 'Ready Fuzzing ..'
#
#fuzzing()
