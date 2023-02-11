from fractions import Fraction

total = Fraction('0')

while True:
    s = input('Enter fraction (press ENTER to quit): ')
    if ',' in s:
        s = s.replace(',', '/')
    s = s.replace(' ', '')
    if not s:
        break
    total += Fraction(s)
    
print('The total is {}.'.format(total))
