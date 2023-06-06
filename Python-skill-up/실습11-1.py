# 의사-난수 게임에서 사용자가 원하는 숫자 범위 입력

import random

def play_the_game():
    user_input = int(input("원하는 숫자를 입력하세요: "))
    answer = random.randint(1, user_input)
    while True:
        guess = int(input("예상 숫자를 입력하세요(0은 종료): "))
        if guess < answer:
            print("숫자가 너무 작습니다. 다시 입력하세요.")
            continue
        elif guess > answer:
            print("숫자가 너무 큽니다. 다시 입력하세요.")
            continue
        elif guess == 0:
            print('종료합니다.')
            break
        else:
            print("정답입니다!")
            break

play_the_game()
