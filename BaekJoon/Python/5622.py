import sys

S = sys.stdin.readline().rstrip()

time = 0

for i in range(len(S)):
    if S[i] in "ABC":
        time += 3
    elif S[i] in "DEF":
        time += 4
    elif S[i] in "GHI":
        time += 5
    elif S[i] in "JKL":
        time += 6
    elif S[i] in "MNO":
        time += 7
    elif S[i] in "PQRS":
        time += 8
    elif S[i] in "TUV":
        time += 9
    elif S[i] in "WXYZ":
        time += 10
    else:
        time += 11

print(time)
