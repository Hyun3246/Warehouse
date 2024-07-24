# 나머지가 같은 부분합끼리의 조합 수가 곧 정답
import sys
input = sys.stdin.readline

N, M = map(int, input().split())

num_list = list(map(int, input().split()))

sum_result = 0      # 부분합 누적을 위한 변수
residue_list = [0]*M       # 나머지 넣기
counter = 0     # 정답 세기

for i in range(N):
    sum_result += num_list[i]
    residue_list[sum_result % M] += 1

for i in range(M):
    counter += (residue_list[i]) * (residue_list[i] - 1) // 2    # 조합(컴비네이션)

print(counter + residue_list[0])
