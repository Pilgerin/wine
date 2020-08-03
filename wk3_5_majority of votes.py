# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 20:45:03 2020

@author: Daria
"""
import random
import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt

def majority_votes(votes):
    #mode, count = ss.mstats.mode(votes)
    vote_array = {}    
    for vote in votes:        
        if vote in vote_array:
            vote_array[vote] += 1            
        else:
            vote_array[vote] = 1
    
    winners=[]
    winner=(max(vote_array.values()))

    for vote, count in vote_array.items():
        if count == winner:
            winners.append(vote)
    
    return random.choice(winners)

votes = [1,2,3,3,1,2,1,3,2,3,3,3,2,2,2]
winner = majority_votes(votes)

def distance(p1,p2):
    return np.sqrt((np.sum(np.power(p2-p1,2))))

points = np.array([[1,2],[3,4],[2,1], [1,3],[4,4], [3,5]])    
p = np.array([0.5, 2])

plt.plot(points[:,0], points[:,1], "ro")
plt.plot(p[0], p[1], 'bo')
plt.axis([0.5,6.0,0.5,6.0])

def find_nearest_neigbors(p, points, k=5):
    distances= np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p, points[i])
    ind = np.argsort(distances)
    return ind[:k]


def knn_predict(p, points, outcomes, k= 5):
    #finds nearest neigbors
    #defines majority of vote based on it
    ind = find_nearest_neigbors(p, points, 3)
    #print (points[ind])
    return majority_votes(outcomes[ind])

outcomes = np.array([0,0,0,0,1,1,1,1,1])
knn_predict(np.array([2.5,2.7]), points, outcomes, k =2 )


def generate_synth_data (n =50):
    """generates random (synthetic) data (a number of 0s and 1s), concatenates them into an array"""  
    points = np.concatenate((ss.norm(0,1).rvs((n,2)),ss.norm(1,1).rvs((n,2))), axis =0)
    outcomes = np.concatenate((np.repeat(0,n), np.repeat(1,n)))
    print (len(points.shape))
    plt.figure()
    plt.plot(points[:n,0],points[:n,1],'ro')
    plt.plot(points[n:,0], points[n:,1],'bo')
    return (points, outcomes)

generate_synth_data()

def make_prediction_grid(predictors, outcomes,limits, h,k):
    """Classifies each point on the prediction grid. 
    Takes j,i (j corresponds to y values rows, x = columns)"""
    (x_min, x_max, y_min, y_max) = limits
    xp = np.arange(x_min, x_max, h)
    yp = np.arange(y_min, y_max, h)
    xx, yy = np.meshgrid(xp, yp)
    
    prediction_grid = np.zeros(xx.shape, dtype = int)
    for i,x in enumerate (xp):
        for j, y in enumerate (yp):
            p = np.array(x,y)
            prediction_grid[j,i] = knn_predict(p, predictors, outcomes,k)
    return (xx, yy, prediction_grid)

(predictors, outcomes) = generate_synth_data()

def plot_prediction_grid (xx, yy, prediction_grid, filename):
    """ Plot KNN predictions for every point on the grid."""
    from matplotlib.colors import ListedColormap
    background_colormap = ListedColormap (["hotpink","lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap (["red","blue","green"])
    plt.figure(figsize =(10,10))
    plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
    plt.scatter(predictors[:,0], predictors [:,1], c = outcomes, cmap = observation_colormap, s = 50)
    plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
    plt.xticks(()); plt.yticks(())
    plt.xlim (np.min(xx), np.max(xx))
    plt.ylim (np.min(yy), np.max(yy))
    plt.savefig(filename)

k = 50; filename='k_5.pdf'; limits = (-3, 4, -3,4); h =0.1

(xx,yy,prediction_grid) = make_prediction_grid(predictors, outcomes,limits, h,k)
plot_prediction_grid(xx,yy,prediction_grid, filename)
