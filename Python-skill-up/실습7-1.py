# 문장 개수 파악 프로그램 (숫자, 빈칸 시작도 파악 가능)

import re


s = ''' 1See the U.S.A. today. It's right here, not
a world away. Average temp. is 66.5.'''

pat= r'[A-Z0-9( )*].*?[.!?](?= [A-Z]|$)'

m = re.findall(pat, s, flags=re.DOTALL | re.MULTILINE)

for i in m:
    print(i)
