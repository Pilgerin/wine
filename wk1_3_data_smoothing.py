import random
import matplotlib.pyplot as plt
random.seed(1)
from pprint import pprint

def moving_window_average(x, n_neighbors=1):
    n = len(x)
    width = n_neighbors*2 + 1
    x = [x[0]]*n_neighbors + x + [x[-1]]*n_neighbors
    return [sum(x[i:(i+width)]) / width for i in range(n)]
    
x = [0,10,5,3,1,5]
print(sum(moving_window_average(x, 1)))

def rand():
    return random.uniform(0,1)

def moving_lots_average(n_neighbors = 1):
    R = 1000
    '''
    x = [random.random() for i in range(R)]
    Y = [x] + [moving_window_average(x, i) for i in range(1, 10)]
    Y[5][9]
    '''
    x = []
    y = []
    minmax_arr = []
    
    for _ in range (R):
        x.append(rand())
        
    for i in range (1,9):
        cur_y = moving_window_average(x,i) 
        maxv = max (cur_y)
        minv = min(cur_y)
        minmax = (maxv - minv)
        #y.append(moving_window_average(x,i))
        y.append(cur_y)
        minmax_arr.append(minmax)       
                               
    print ('Y[5][9]', y[5][9])
    pprint (minmax_arr)
    
    ranges = [max(x) - min(x) for x in y]
    pprint(ranges)
    
if __name__ == "__main__":
    print('called', end=' ')
    moving_lots_average(5)

