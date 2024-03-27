import sys

# 자릿수의 합 구하는 함수
def digit_sum(num):
    sum_result = 0
    while num > 0:
        sum_result += num % 10
        num = num  // 10
    return sum_result


N = int(sys.stdin.readline().strip())

answer = 0

for i in range(N):
    answer = digit_sum(i) + i
    if answer == N:
        print(i)
        break
    else:
        answer = 0

if answer == 0:
    print(0)
