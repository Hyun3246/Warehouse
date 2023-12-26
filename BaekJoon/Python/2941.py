import sys

S = sys.stdin.readline().strip()

croatia_alphabet = ["c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="]

for i in croatia_alphabet:
    S = S.replace(i, "a")

print(len(S))
