import sys

score_list = []

for i in range(20):
    A, B, C = sys.stdin.readline().strip().split()
    B = float(B)
    score_tuple = B, C
    score_list.append(score_tuple)

score_list = [(i, j) for (i, j) in score_list if j != "P"]    # List comprehension

tot_score = 0

for i in score_list:
    if i[1] == "A+":
        tot_score += (4.5*i[0])
    elif i[1] == "A0":
        tot_score += (4.0*i[0])
    elif i[1] == "B+":
        tot_score += (3.5*i[0])
    elif i[1] == "B0":
        tot_score += (3.0*i[0])
    elif i[1] == "C+":
        tot_score += (2.5*i[0])
    elif i[1] == "C0":
        tot_score += (2.0*i[0])
    elif i[1] == "D+":
        tot_score += (1.5*i[0])
    elif i[1] == "D0":
        tot_score += (1.0*i[0])
    else:
        tot_score += (0.0*i[0])

tot_point = 0

for i in score_list:
    tot_point += i[0]

print(round(tot_score/tot_point, 6))
