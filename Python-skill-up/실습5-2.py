# 5 X 5 테이블 형태의 2차원 배열 프로그램(정수로 출력)

num_table = [
    [1, 2, 3, 4, 5],
    [11, 55, 100, 225, 6449],
    [1, 1, 8, 98, 9],
    [4, 5, 777, 848, 9999],
    [156, 15651, 1303, 654, 0]
]

max_width = -1
for x in num_table:
    for y in x:
        if y > max_width:
            max_width = y

max_width = len(str(max_width))


for i in num_table:
    for j in i:
        print('{:>{}d}'.format(j, max_width), end=' ')
    print()
