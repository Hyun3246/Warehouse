import sys

A, B, C = map(int, sys.stdin.readline().strip().split())

tri_list = [A, B, C]
max_num = max(tri_list)
tri_list.remove(max_num)

if max_num == sum(tri_list):
    print(A + B + C - 1)
elif max_num > sum(tri_list):
    print(sum(tri_list)*2-1)
else:
    print(A + B + C)
