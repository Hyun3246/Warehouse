import sys

matrix = []

for i in range(9):
    row = list(map(int, sys.stdin.readline().strip().split()))
    matrix.append(row)

max_num, max_row, max_col = 0, 0, 0

for i in range(9):
    for j in range(9):
        if matrix[i][j] >= max_num:
            max_num = matrix[i][j]
            max_row = i + 1
            max_col = j + 1

print(max_num)
print(max_row, max_col)
