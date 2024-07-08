import sys
input = sys.stdin.readline

N, M = map(int, input().split())

words = [input().strip() for _ in range(N)]

word_dict = dict()

for i in words:
    if len(i) < M:
        continue
    else:
        if i in word_dict:
            word_dict[i] += 1
        else:
            word_dict[i] = 1


word_dict = sorted(word_dict.items(), key = lambda x : (-x[1], -len(x[0]), x[0]))

for i in word_dict:
    print(i[0])
