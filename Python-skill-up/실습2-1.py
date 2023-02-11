# 모음과 자음 숫자 세기 프로그램

new_str = input("문자열을 입력하세요: ")

ja = 0
mo = 0

for i in new_str:
    if i.upper() in 'AEIOU':
        mo += 1
    elif i == ' ':
        pass
    else:
        ja += 1

print("자음 개수: {}, 모음 개수: {}".format(ja, mo))
