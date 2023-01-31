import math

def cal_hypotenuse(bottom, angle):
    angle = math.radians(angle)
    hypotenuse = bottom / math.cos(angle)
    return hypotenuse

print(cal_hypotenuse(5, 30))