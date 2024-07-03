import sys
input = sys.stdin.readline

people_list = set()

people_list.add("ChongChong")

N = int(input())

counter = 1

while True:
    people = list(input().strip().split())
    
    if "ChongChong" not in people:
        counter += 1
        continue
    else:
        for i in people:
            people_list.add(i)
        break


for i in range(N-counter):
    a, b = input().strip().split()

    if a in people_list:
        people_list.add(b)
    if b in people_list:
        people_list.add(a)
        

print(len(people_list))
