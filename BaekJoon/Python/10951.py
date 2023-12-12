# sys.stdin.readline()를 사용한 코드
import sys

while True:
    try:
        A, B = map(int, sys.stdin.readline().split(" "))
        print(A + B)
    except:
        break
        
# input을 사용한 코드
while True:
    try:
        A, B = map(int, input().split(" "))
        print(A + B)
    except EOFError:
        break
