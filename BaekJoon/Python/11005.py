import sys

N, B = map(int, sys.stdin.readline().strip().split()) 

arr = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
answer = ''

while N > 0:
    answer += str(arr[N % B])
    N //= B

print(answer[::-1])
