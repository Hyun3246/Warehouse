import sys

answer_x = 0
answer_y = 0

x1, y1 = map(int, sys.stdin.readline().strip().split())
x2, y2 = map(int, sys.stdin.readline().strip().split())
x3, y3 = map(int, sys.stdin.readline().strip().split())

if x1 == x2:
    answer_x = x3
elif x1 == x3:
    answer_x = x2
else:
    answer_x = x1

if y1 == y2:
    answer_y = y3
elif y1 == y3:
    answer_y = y2
else:
    answer_y = y1

print(answer_x, answer_y)
