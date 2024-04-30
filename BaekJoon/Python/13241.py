import sys

def get_least_common_multiple(a, b):
    greatest_common_divisor = 1

    if a < b:
        for i in range(1, a + 1):
            if (a % i == 0) and (b % i == 0):
                greatest_common_divisor = i
    else:
        for i in range(1, b + 1):
            if (a % i == 0) and (b % i == 0):
                greatest_common_divisor = i

    least_common_multiple = int(a * b / greatest_common_divisor)

    return least_common_multiple
    
A, B = map(int, sys.stdin.readline().strip().split())

print(get_least_common_multiple(A, B))
