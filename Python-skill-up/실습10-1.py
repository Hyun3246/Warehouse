from decimal import Decimal

sign = int(input("부호를 입력하세요(1은 양수, 0은 음수): "))

number = []

while True:
    num = input("원하는 숫자를 앞 자리부터 하나씩 입력하세요(아무것도 입력하지 않으면 종료): ")
    if num:
        number.append(int(num))
        continue      
    else:
        break

number = tuple(number) 

cipher = int(input("자릿수를 입력하세요: "))

final_number = (sign, number, cipher)

decimal_form = Decimal(final_number)

print(decimal_form)
