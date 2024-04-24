import sys

N = int(sys.stdin.readline().strip())

num_list = list(map(int, sys.stdin.readline().strip().split()))

one_num_list = set(num_list)
one_num_list = list(one_num_list)
one_num_list.sort()

dic = {one_num_list[i]: i for i in range(len(one_num_list))}

for i in num_list:
    print(dic[i], end=" ")
