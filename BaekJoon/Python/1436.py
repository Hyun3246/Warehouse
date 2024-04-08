import sys

N = int(sys.stdin.readline().strip())

counter = 0
num = 0

while True:
    num = str(num)
    if "666" in num:
        counter += 1
        pass

    num = int(num)

    if counter == N:
        break
    num += 1
    
print(num)
