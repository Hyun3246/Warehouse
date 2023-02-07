import numpy as np
from time import time

def benchmarks():
    t1 = time()
    python_list = list(range(1, 1_000_001))
    t2 = time()
    python_list_time = t2 - t1
    
    t1 = time()
    tot = sum(python_list)
    t2 = time()
    python_list_sum_time = t2 - t1

    t1 = time()
    numpy_list = np.arange(1, 1_000_001)
    t2 = time()
    numpy_list_time = t2 - t1

    t1 = time()
    tot = np.sum(numpy_list)
    t2 = time()
    numpy_list_sum_time = t2 - t1

    print("Python list time: {}".format(python_list_time))
    print("Python list sum time: {}".format(python_list_sum_time))
    print("Numpy list time: {}".format(numpy_list_time))
    print("Numpy list sum time: {}".format(numpy_list_sum_time))

benchmarks()