import sys

S = sys.stdin.readline().strip()

S = S.upper()

alphabet = dict()

for i in S:
    if i in alphabet.keys():
        alphabet[i] += 1
    else:
        alphabet[i] = 1

max_list = [k for k, v in alphabet.items() if max(alphabet.values())== v]    # alphabet 딕셔너리 value의 최댓값과 같은 경우, key를 리스트에 포함한다.

if len(max_list) == 1:
    print(max_list[0])
else:
    print("?")
