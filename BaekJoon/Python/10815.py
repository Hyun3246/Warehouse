import sys

N = int(sys.stdin.readline().strip())

real_card = list(map(int, sys.stdin.readline().strip().split()))

M = int(sys.stdin.readline().strip())

question = list(map(int, sys.stdin.readline().strip().split()))

card_dict = {i: i for i in real_card}

for i in question:
    if i in card_dict:
        print(1, end=" ")
    else:
        print(0, end=" ")
