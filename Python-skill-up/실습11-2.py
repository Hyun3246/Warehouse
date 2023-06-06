# 직각삼각형의 밑변과 각도 이용해서 빗변 길이 구하기

import math

def cal_hypotenuse(bottom, angle):
    angle = math.radians(angle)
    hypotenuse = bottom / math.cos(angle)
    return hypotenuse

print(cal_hypotenuse(5, 30))
