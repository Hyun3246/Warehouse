import numpy as np

a = np.arange(1, 100)

a = (a == 1) | (a %3 == 0) | (a > 75)

print(a)
