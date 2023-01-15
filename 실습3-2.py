# 리스트 평균값 & 중앙값 계산 프로그램

user_list = input("리스트 숫자를 입력하세요: ").split(', ')

user_list = [int(i) for i in user_list]

user_list.sort()

if len(user_list) % 2 == 0:
    mid = (user_list[len(user_list) // 2 - 1] + user_list[len(user_list) // 2]) / 2
else:
    mid = user_list[(len(user_list) - 1) // 2]


print(user_list)
print(mid)