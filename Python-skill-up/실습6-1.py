# 전화번호 지역코드 포맷 검증 프로그램

import re

def follow_the_rule(number):
    if re.match(r'\d{3}[- ]', number):
        return 'Correct'
    else:
        return 'Error'

print(follow_the_rule('393-4460'))
