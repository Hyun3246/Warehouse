import sys

N, M = map(int, sys.stdin.readline().strip().split())

board = []

w_first_board = ["WBWBWBWB", "BWBWBWBW","WBWBWBWB", "BWBWBWBW","WBWBWBWB", "BWBWBWBW","WBWBWBWB", "BWBWBWBW"]
b_first_board = ["BWBWBWBW","WBWBWBWB", "BWBWBWBW","WBWBWBWB", "BWBWBWBW","WBWBWBWB", "BWBWBWBW", "WBWBWBWB"]


min_flip = 64

for i in range(N):
    line = sys.stdin.readline().strip()
    board.append(line)

# 체스판 만들기
for i in range(N-7):
    for j in range(M-7):
        chess_board = []
        for k in range(8):
            chess_board.append(board[i+k][j:j+8])
        
        flip_num = 0

        # 정답 체스판과 비교
        if chess_board[0][1] == "W":
            for l in range(8):
                for p in range(8):
                    if w_first_board[l][p] != chess_board[l][p]:
                        flip_num += 1
        else:
            for l in range(8):
                for p in range(8):
                    if b_first_board[l][p] != chess_board[l][p]:
                        flip_num += 1

        if flip_num > 32:
            flip_num = 64 - flip_num

        if flip_num < min_flip:
            min_flip = flip_num

print(min_flip)
