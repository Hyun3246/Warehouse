# 0 ~ 99 숫자 중 1이거나 3의 배수이거나 75보다 큰 숫자 제외하고 마스크

import numpy as np

a = np.arange(1, 100)

print(a[(a == 1) | (a % 3 == 0) | (a > 75)])
