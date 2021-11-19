import math
import random
import sys
import numpy as np

#examples = [[6.8248, 5.2187, -2.5425, 0.5461, -1], [-0.74324, -0.32902, -0.42785, 0.23317, 1.0], [-1.6637, 3.2881, -2.2701, -2.2224, 1.0], [-1.4174, -2.2535, 1.518, 0.61981, 1.0], [-0.071503, 3.7412, -4.5415, -4.2526, 1.0], [5.1129, -0.49871, 0.62863, 1.1189, -1], [-2.9138, -9.4711, 9.7668, -0.60216, 1.0], [-1.0112, 2.9984, -1.1664, -1.6185, 1.0], [2.9421, 7.4101, -0.97709, -0.88406, -1], [4.3848, -3.0729, 3.0423, 1.2741, -1]]
examples = [[2,2],[3,4],[2,1]]
x = np.array(examples)
a = np.ones(len(x))
y = np.ones(len(x))
random.seed(3)
for i in range(len(x)):
    a[i] *= random.randrange(1,5)
    y[i] += random.randrange(0,2)
sum = 0
sum2 = 0
xs = []
asum = []
for i in range(len(x)):
    ina = []
    xsin = []
    for j in range(len(x)):
        others = a[i]*a[j]*y[i]*y[j]
        sum += np.inner(x[i],x[j])*others
        
        asum.append( a[i]*y[i]*a[j]*y[j])
        xs.append(np.inner(x[i],x[j]))
val = 0
#asum = [4.0, 4.0, 6.0, 4.0, 4.0, 6.0, 6.0, 6.0, 9.0]
val = np.sum(x*y*a)
print(sum)
print(val)
print()