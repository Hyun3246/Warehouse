# 문자열의 앞 두 글자와 끝 두 글자 삭제 프로그램

def Eraser(str):
    str = str[2:]
    str = str[:-2]
    
    return str

print(Eraser("안녕하쌉사리와요"))