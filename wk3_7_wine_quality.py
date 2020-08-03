# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 18:27:35 2020

@author: Daria
"""
import numpy as np
from numpy import random
import pandas as pd
import scipy.stats as ss
import sklearn.preprocessing, sklearn.decomposition
import random 

def majority_vote_fast(votes):
    mode, count = ss.mstats.mode(votes)
    return mode

def distance(p1, p2):
    return np.sqrt(np.sum(np.power(p2 - p1, 2)))

def find_nearest_neighbors(p, points, k=5):
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p, points[i])
    ind = np.argsort(distances)
    return ind[:k]

def knn_predict(p, points, outcomes, k=5):
    ind = find_nearest_neighbors(p, points, k)
    return majority_vote_fast(outcomes[ind])[0]

wine=pd.read_csv(r'asset-v1_HarvardX+PH526x+2T2019+type@asset+block@wine.csv')

numeric_data = wine
numeric_data['is_red'] = (wine['color']=='red').astype(int)
numeric_data=numeric_data.drop(['color','high_quality','quality'], axis =1)
#print (numeric_data.groupby('is_red').count())

numeric_data = sklearn.preprocessing.scale(numeric_data)
clean = sklearn.decomposition.PCA(n_components=2)
principal_components = clean.fit_transform(numeric_data)
#print(principal_components.shape)

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
#from matplotlib.backends.backend_pdf import PdfPages
observation_colormap = ListedColormap(['red', 'blue'])
x = principal_components[:,0]
y = principal_components[:,1]

plt.title("Principal Components of Wine")
plt.scatter(x, y, alpha = 0.2, c = wine['high_quality'], cmap = observation_colormap, edgecolors = 'none')
plt.xlim(-8, 8); plt.ylim(-8, 8)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

np.random.seed(1)
x = np.random.randint(0, 2, 1000)
y = np.random.randint(0 ,2, 1000)

def accuracy(predictions, outcomes):    
    #if predictions.shape==outcomes.shape:
    #    print(np.count_nonzero(predictions))
     #   print(np.count_nonzero(outcomes))       
    return 100*np.mean(predictions == outcomes)
    
print('Accuracy of X predicting Y: ', accuracy(x,y))
print('What proportion of wines in the dataset are of low quality?', accuracy(0,wine['high_quality']))

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(numeric_data, wine['high_quality'])
library_predictions = knn.predict(numeric_data)
print('Accuracy of library predicting high quality wine: ', accuracy(library_predictions, wine["high_quality"]))

random.seed(123)
n_rows = wine.shape[0]
selection = random.sample(range(n_rows), 10)
print (selection)

predictors = np.array(numeric_data)
print(predictors)
training_indices = [i for i in range(len(predictors)) if i not in selection]
outcomes = np.array(wine["high_quality"])

my_predictions = np.array([knn_predict(p, predictors[training_indices,:], outcomes[training_indices],5) for p in predictors[selection]])
percentage = accuracy(my_predictions, wine.high_quality.iloc[selection])
print (percentage)