import sys

num_list = list()    # 나머지 몽땅 넣는 리스트

for i in range(10):
    num = int(sys.stdin.readline())
    num = num % 42
    num_list.append(num)

answer = 0    # 서로 다른 나머지 개수 세는 변수
same_list = list()    # 서로 다른 나머지 넣는 리스트

for i in num_list:
    if i not in same_list:    # 나머지가 나머지만 넣은 리스트에 없으면
        answer += 1
        same_list.append(i)

print(answer)
