# 1로 채워진 10 X 10 배열을 생성한 뒤 가운데 부분을 0으로 만들기

import numpy as np

a = np.ones((10, 10), dtype='int')

print(a)

a[1:9, 1:9] = 0

print(a)
