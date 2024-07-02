import math
import sys
input = sys.stdin.readline

T = int(input())

for i in range(T):
    N, M = map(int, input().split())
    print(math.factorial(M)//(math.factorial(N)*math.factorial(M-N)))
