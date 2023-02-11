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
