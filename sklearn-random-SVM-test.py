
from random import *

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


data = []
data_class = []

for index in range(100) :
    data.append([randint(10,20),randint(5,10)])
    data_class.append(0)
    data.append([randint(5,10),randint(0,5)])
    data_class.append(1)
    data.append([randint(0,5),randint(5,10)])
    data_class.append(2)

x_train, x_test, y_train, y_test = train_test_split(data, data_class, test_size=.4, random_state=42)
classfy = SVC(gamma=2, C=1)

classfy.fit(x_train,y_train)

score = classfy.score(x_test, y_test)

print 'Classfy Score:' , score

test_data_list = []
test_data_classfy = []

for index in range(10) :
    test_data = [[randint(0,20),randint(5,10)]]
    test_data_predict = classfy.predict(test_data)
    
    print test_data , test_data_predict
    
    test_data_list += test_data
    test_data_classfy.append(test_data_predict)
    
plt.figure('Train Data')

for index,class_index in zip(data,data_class) :
    color = ''
    
    if 0 == class_index :
        color = '#F00000'
    elif 1 == class_index :
        color = '#0F0000'
    elif 2 == class_index :
        color = '#00F000'
        
    plt.scatter(index[0],index[1],c = color)
    
for index in test_data_list :
    plt.scatter(index[0],index[1],c = '#0000FF')
    
plt.show()

