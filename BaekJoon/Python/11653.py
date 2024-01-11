import sys

N = int(sys.stdin.readline().strip())
M = N
while True:
    for i in range(2, M + 1):
        while True:
            if N % i == 0:
                print(i)
                N /= i
            else:
                break
        if N == 1:
            break
    if N == 1:
            break        
