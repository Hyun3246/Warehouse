'''idea: 배경을 0으로 이루어진 2차원 배열로 만들고, 
사각형이 들어가는 곳은 1로 만들자.
'''

import sys

background = [[0]*101 for i in range(101)]

N = int(sys.stdin.readline().strip())

for i in range(N):
    width, height = map(int, sys.stdin.readline().strip().split())
    for j in range(10):
        for k in range(10):
            background[height + j][width + k] = 1

area = 0

for i in range(101):
    area += background[i].count(1)

print(area)
