import sys

input = sys.stdin.readline

while True:
    string = input().rstrip()
    if string == ".":
        break
    
    stack = []

    for j in string:        
        if j == "(" or j == "[":
            stack.append(j)
 
        elif j == ")":
            if len(stack) != 0 and stack[-1] == '(':
                stack.pop()

            else:
                stack.append(')')
    
        elif j == "]":
            if len(stack) != 0 and stack[-1] == '[':
                stack.pop()
   
            else:
                stack.append(']')
 
        else:
            pass

    if len(stack) == 0:
        print("yes")
    else:
        print("no")
