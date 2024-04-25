import sys

string = sys.stdin.readline().strip()

set_of_string = set()

for i in range(len(string)):
    for j in range(len(string)):
        sub_string = string[i:j+1]
        set_of_string.add(sub_string)

print(len(set_of_string)-1)
