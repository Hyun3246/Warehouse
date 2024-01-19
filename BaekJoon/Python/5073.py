import sys

while True:
    A, B, C = map(int, sys.stdin.readline().strip().split())
    if A == B == C == 0:
        break

    tri_list = [A, B, C]
    max_num = max(tri_list)
    tri_list.remove(max_num)
    
    if max_num >= sum(tri_list):
        print("Invalid")
    elif A == B == C:
        print("Equilateral")
    elif (A == B) or (C == B) or (A == C):
        print("Isosceles")
    else:
        print("Scalene")

