import sys
input = sys.stdin.readline

T = int(input())

for i in range(T):
    j = 0
    counter = 0
    string = input().strip()

    for j in string:        
        if j == "(":
            counter += 1
        else:
            counter -= 1

        if counter < 0:
            break
    
    if counter == 0:
        print("YES")
    else:
        print("NO")
