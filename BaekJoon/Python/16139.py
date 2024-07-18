import sys
input = sys.stdin.readline
S = input().strip()

app_let_list = [[0] * 26]

for i, v in enumerate(S):
    app_let_list.append(app_let_list[i][:])
    app_let_list[i+1][ord(v)-97] += 1

q = int(input())

for i in range(q):
    letter, start, end = input().split()
    start = int(start)
    end = int(end)
    print(app_let_list[end + 1][ord(letter)-97] - app_let_list[start][ord(letter)-97])
    
