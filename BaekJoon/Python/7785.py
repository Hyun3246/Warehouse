import sys

N = int(sys.stdin.readline().strip())

employee = dict()

for i in range(N):
    name, status = sys.stdin.readline().strip().split()
    if status == "enter":
        employee[name] = 0
    else:
        del employee[name]

now_list = list(employee.keys())
now_list.sort(reverse=True)

for i in now_list:
    print(i)
