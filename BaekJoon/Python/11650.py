import sys

N = int(sys.stdin.readline().strip())

loca_list = []

for i in range(N):
    x, y = map(int, sys.stdin.readline().strip().split())
    loca = (x, y)
    loca_list.append(loca)

loca_list.sort(key = lambda x: (x[0], x[1]))

for i in loca_list:
    print(i[0], i[1])
