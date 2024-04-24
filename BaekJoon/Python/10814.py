import sys

N = int(sys.stdin.readline().strip())

member_info_list = []

for i in range(N):
    age, name = sys.stdin.readline().strip().split()
    age = int(age)
    member_info = (age, name, i)
    
    member_info_list.append(member_info)

member_info_list.sort(key = lambda x: (x[0], x[2]))

for i in member_info_list:
    print(i[0], i[1])
