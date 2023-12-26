import sys

N = int(sys.stdin.readline().strip())

words = []


for i in range(N):
    S = sys.stdin.readline().strip()
    words.append(S)

for j in words:
    alphabet_list = []
    for k in range(1, len(j)):
        alphabet_list.append(j[0])
        if j[k-1] == j[k]:
            pass
        else:
            if j[k] in alphabet_list:
                N-=1
                break
            else:
                alphabet_list.append(j[k])
                
print(N)
