import sys

N = int(sys.stdin.readline().strip())

x_list = []
y_list = []

for i in range(N):
    x, y = map(int, sys.stdin.readline().strip().split())
    x_list.append(x)
    y_list.append(y)

try:
    print((max(x_list) - min(x_list))*(max(y_list) - min(y_list)))
except:
    print(0)
