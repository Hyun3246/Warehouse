import sys
input = sys.stdin.readline

N, M = map(int, input().split())

num_list = list(map(int, input().split()))

sum_results = [0]

for i in range(N):
    sum_results.append(sum_results[i] + num_list[i])

for _ in range(M):
    i, j = map(int, input().split())
    print(sum_results[j]-sum_results[i-1])
