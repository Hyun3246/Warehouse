import sys
input = sys.stdin.readline

N = int(input())

real_div = list(map(int, input().split()))

real_div.sort()

print(real_div[-1] * real_div[0])
