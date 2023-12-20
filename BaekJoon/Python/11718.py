import sys

inputs = []

while True:
    S = sys.stdin.readline().rstrip()
    if S == "":
        break
    else:
        inputs.append(S)
        

for i in inputs:
    print(i)
