import sys

x, y, w, h = map(int, sys.stdin.readline().strip().split())

path_length = [x, y, w-x, h-y]

print(min(path_length))
