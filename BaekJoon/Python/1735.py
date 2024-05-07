import sys

# 유클리드 호제법 사용

def Euclidean(a, b):
    while b != 0:
        [a, b] = [b, a % b]
    return a

A, B = map(int, sys.stdin.readline().strip().split())
C, D = map(int, sys.stdin.readline().strip().split())

denominator = int(B * D / Euclidean(B, D))

numerator = int((A * denominator / B) + (C * denominator / D))

abbreviation = Euclidean(denominator, numerator)

denominator /= abbreviation

numerator /= abbreviation

print(int(numerator), int(denominator))
