import sys

student_list = list(range(1, 30 + 1))

for i in range(28):
    remove_num = int(sys.stdin.readline())
    student_list.remove(remove_num)

print(min(student_list))
print(max(student_list))
