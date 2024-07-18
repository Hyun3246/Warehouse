import sys
input = sys.stdin.readline

N, K = map(int, input().split())

num_list = list(map(int, input().split()))

sum_results = [0]

for i in range(N):
    sum_results.append(sum_results[i] + num_list[i])

max_val = -1000

for i in range(N-K+1):
    if max_val < sum_results[i + K] - sum_results[i]:
        max_val = sum_results[i + K] - sum_results[i]
    
print(max_val)
