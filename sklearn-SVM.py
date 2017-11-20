from __future__ import print_function

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


X, y = make_moons(noise=0.3, random_state=0)
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4, random_state=42)

svc_model = SVC(gamma=2, C=1)

svc_model.fit(X_train,y_train)

score = svc_model.score(X_test, y_test)

print(score)

predict = svc_model.predict(X_test)

for x_index ,y_index ,y_predict in zip(X_test,y_test,predict) :
    if not y_index == y_predict :
        print('ERR ' ,x_index,y_index,y_predict)

        