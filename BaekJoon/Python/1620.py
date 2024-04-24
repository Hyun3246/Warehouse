import sys

N, M = map(int, sys.stdin.readline().strip().split())

answer = dict()
question_list = []


for i in range(N):
    name = sys.stdin.readline().strip()
    answer[name] = str(i+1)

answer_1 = {v:k for k,v in answer.items()}

for j in range(M):
    question = sys.stdin.readline().strip()
    question_list.append(question)

for p in question_list:
    if p in answer:
        print(answer.get(p))
    else:
        print(answer_1.get(p))
