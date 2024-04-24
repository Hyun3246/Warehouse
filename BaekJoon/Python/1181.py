import sys

N = int(sys.stdin.readline().strip())

voca_list = []
voca_info_list = []

for i in range(N):
    voca = sys.stdin.readline().strip()
    if voca in voca_list:
        pass
    else:
        voca_list.append(voca)
        voca_info = (voca, len(voca))
        voca_info_list.append(voca_info)

voca_info_list.sort(key = lambda x: (x[1], x[0]))

for i in voca_info_list:
    print(i[0])
