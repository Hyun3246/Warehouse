# 전화번호 앞에 숫자 1 추가

import re

def add_one_at_front(number):
    if re.match(r'\d{3}[- ]\d{3}[- ]\d{4}', number):
        return '1' + number
    else:
        return 'Error'

print(add_one_at_front('010-393-4460'))