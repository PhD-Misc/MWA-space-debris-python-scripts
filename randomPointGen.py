import numpy as np
import matplotlib.pyplot as plt

import random


numberOfPoints = 200
data = np.zeros((2000,2000))

for n in range(numberOfPoints):
    x = random.randrange(0, 2000)
    y = random.randrange(0, 2000)
    if 1 < x < 1995 and 1 < y < 1995:
        data[x,y] = 1
        data[x+1,y] =1
        data[x,y+1] = 1
        data[x-1,y] = 1
        data[x,y-1] =1
    print("generating point number " + str(n) + " at x " + str(x) + " and y " + str(y) )

plt.imshow(data, cmap=plt.cm.inferno, origin='lower')
plt.show()
