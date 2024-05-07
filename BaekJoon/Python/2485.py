import sys

# 유클리드 호제법 사용

def Euclidean(a, b):
    while b != 0:
        [a, b] = [b, a % b]
    return a

N = int(sys.stdin.readline().strip())

current_local = [int(sys.stdin.readline().strip()) for i in range(N)]

intervals = [(current_local[i + 1] - current_local[i]) for i in range(N-1)]

for i in range(len(intervals) - 1):
    gcd = Euclidean(intervals[i], intervals[i + 1])
    if gcd == 1:
        break
    else:
        intervals[i + 1] = gcd

tot_length = current_local[-1] - current_local[0]

answer = int(tot_length // gcd) - N + 1

print(answer)
