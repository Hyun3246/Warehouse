from collections import defaultdict
import sys
input = sys.stdin.readline

users = defaultdict(int)

N = int(input())

counter = 0

for i in range(N):
    id = input().strip()
    if id == "ENTER":
        users = defaultdict(int)
    else:
        if id not in users.keys():
            users[id] = 1
            counter += 1    

print(counter)
