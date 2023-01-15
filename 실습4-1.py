# 별표 행렬 출력 프로그램

import time

def make_timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print("소요시간: ", t2 - t1)
    return wrapper

@make_timer
def print_stars_1():
    for i in range(20):
        return '*' * 20

@make_timer
def print_stars_2():
    a = ''.join(['*'] * 20)
    a = (a + '\n') * 20
    return a

print(print_stars_1())
print(print_stars_2())