import sys

matrix = []

for i in range(5):
    row = []
    string = sys.stdin.readline().strip()
    for j in range(len(string)):
        row.append(string[j])
    matrix.append(row)


for i in range(15):
    for j in range(5):
        try:
            print(matrix[j][i], end="")
        except:
            continue
