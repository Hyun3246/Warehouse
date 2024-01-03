import sys

def path_num(N):
    result = 0
    i = 0
    if N == 0:
        result = 1
    else:
        while N > 0:
            result += 1
            N = N - (i * 6)
            i += 1

    return result

N = int(sys.stdin.readline().strip())
N = N-1

print(path_num(N))
