import sys

numbers = []

N, k = map(int, sys.stdin.readline().strip().split())

scores = list(map(int, sys.stdin.readline().strip().split()))

scores.sort()

cut_line = scores[-k]

print(cut_line)
