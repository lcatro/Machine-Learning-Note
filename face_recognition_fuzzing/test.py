
import face_recognition

def load_image_encoding(file_path) :
    image = face_recognition.load_image_file(file_path)
    image_encoding = face_recognition.face_encodings(image)[0]
    
    return image_encoding


face_data = []

face_data.append(load_image_encoding('obama/obama.jpg'))
face_data.append(load_image_encoding('obama/obama2.jpg'))
face_data.append(load_image_encoding('biden/biden.jpg'))
face_data.append(load_image_encoding('ponyma/ponyma.png'))

test_obama = load_image_encoding('test/obama.png')
test_biden = load_image_encoding('test/biden.png')
test_ponyma = load_image_encoding('test/ponyma.png')


print 'Obama Test:'
print face_recognition.compare_faces(face_data, test_obama),\
      face_recognition.face_distance(face_data, test_obama)
print 'Biden Test:'
print face_recognition.compare_faces(face_data, test_biden),\
      face_recognition.face_distance(face_data, test_biden)
print 'PonyMa Test:'
print face_recognition.compare_faces(face_data, test_ponyma),\
      face_recognition.face_distance(face_data, test_ponyma)


