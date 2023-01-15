# 입력한 숫자보다 작은 모은 완전제곱수 출력

def square(n):
    for i in range(n):
        yield i * i



my_input = int(input("정수를 입력하시오: "))


if my_input in square(my_input):
    print(True)
else:
    print(False)