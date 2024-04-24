import sys

N = map(int, sys.stdin.readline().strip())
card_list = list(map(int, sys.stdin.readline().strip().split()))
M = map(int, sys.stdin.readline().strip())
question = list(map(int, sys.stdin.readline().strip().split()))

card_dict = dict()

for i in card_list:
    if i not in card_dict:
        card_dict[i] = 1
    else:
        card_dict[i] += 1

for j in question:
    if j in card_dict:
        print(card_dict[j], end=" ")
    else:
        print(0, end=" ")
