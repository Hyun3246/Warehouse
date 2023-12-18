import sys

N = int(sys.stdin.readline())
scores = list(map(int, sys.stdin.readline().split()))

max_score = max(scores)

for i in range(N):
    scores[i] = scores[i]/max_score*100

print(sum(scores)/N)
