import sys

def dot_num(N):
    result = 2
    for i in range(N):
        result = result * 2 - 1
    
    return (result ** 2)

N = int(sys.stdin.readline().strip())

print(dot_num(N))
