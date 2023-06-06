# 5 X 5 X 5 큐브의 가운데 3 X 3 X 3 부분은 0으로 만들기

import numpy as np

a = np.ones((5, 5, 5), dtype='int')

a[1:4, 1:4, 1:4] = 0

print(a)
