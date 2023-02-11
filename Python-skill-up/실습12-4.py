import numpy as np

a = np.ones((10, 10), dtype='int')

print(a)

a[2:8, 2:8] = 0

print(a)
