# Fraction 클래스를 이용한 분수 덧셈 계산기

from fractions import Fraction

total = Fraction('0')

while True:
    s = input('Enter fraction (press ENTER to quit): ')
    if ',' in s:
        s = s.replace(',', '/')
    s = s.replace(' ', '')      # 사용자가 빈칸을 입력하는 경우 방지
    if not s:
        break
    total += Fraction(s)
    
print('The total is {}.'.format(total))
