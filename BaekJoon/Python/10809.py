import sys

S = sys.stdin.readline().rstrip()
alphabet = "abcdefghijklmnopqrstuvwxyz"

for i in alphabet:
    print(S.find(i), end=" ")    # find는 없으면 -1, index는 없으면 오류 반환
