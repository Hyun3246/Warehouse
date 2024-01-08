import sys

X = int(sys.stdin.readline().strip())
line = 1

#  몇 번째 줄인지 구하기
while X > line:
    X -= line
    line += 1
    
# 줄이 짝수일 경우
if line % 2 == 0:
    a = X
    b = line - X + 1
# 줄이 홀수일경우
elif line % 2 == 1:
    a = line - X + 1
    b = X

print(a, '/', b)
            
