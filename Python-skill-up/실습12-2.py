# numpy 패키지로 1000 X 1000 배열 생성 속도 측정 & 평균과 표준편차 구하기

import numpy as np
from time import time

t1 = time()
a = np.random.rand(1000000)
a = a.reshape(1000, 1000)
t2 = time()

print(a)
print("배열의 생성 시간은 {}입니다.".format(t2 - t1))

print(np.mean(a))
print(np.std(a))
