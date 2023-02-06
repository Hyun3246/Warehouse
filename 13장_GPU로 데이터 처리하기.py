import numpy as np
import cupy as cp
import time

# Numpy는 CPU 사용
start_time = time.time()
myvar_cpu = np.ones((800, 800, 800))
end_time = time.time()
print(end_time - start_time)

# CuPy는 GPU 사용
start_time = time.time()
myvar_cpu = cp.ones((800, 800, 800))
cp.cuda.Stream.null.synchronize()
end_time = time.time()
print(end_time - start_time)

