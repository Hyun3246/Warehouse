import sys
input = sys.stdin.readline

N = int(input())

# 창문 개수의 루트를 씌운 수의 정수 부분만큼 열려있다.
print(int(N**(1/2)))
