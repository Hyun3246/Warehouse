import numpy as np

a = np.ones((5, 5, 5), dtype='int')

a[2:5, 2:5, 2:5] = 0

print(a)
