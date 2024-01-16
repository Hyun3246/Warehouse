import sys

A = int(sys.stdin.readline().strip())
B = int(sys.stdin.readline().strip())
C = int(sys.stdin.readline().strip())

if A + B + C != 180:
    print("Error")
elif A == B == C:
    print("Equilateral")
elif A == B or B == C or C == A:
    print("Isosceles")
else:
    print("Scalene")
