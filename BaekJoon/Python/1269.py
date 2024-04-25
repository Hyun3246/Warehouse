import sys

name_set_1 = set()

N, M = map(int, sys.stdin.readline().strip().split())

set_a = set(map(int, sys.stdin.readline().strip().split()))
set_b = set(map(int, sys.stdin.readline().strip().split()))

set_a_b = set.intersection(set_a, set_b)

len_set_a = len(set_a) - len(set_a_b)
len_set_b = len(set_b) - len(set_a_b)

print(len_set_a + len_set_b)
