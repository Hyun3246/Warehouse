import sys

T = int(sys.stdin.readline().rstrip())

for i in range(T):
    repeat, string = sys.stdin.readline().split()
    repeat = int(repeat)
    for j in range(len(string)):
        print(string[j]*repeat, end="")
        
    print()
