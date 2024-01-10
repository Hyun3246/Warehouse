import sys

while True:
    numbers = []
    n = int(sys.stdin.readline().strip())

    if n == -1:
        break
    
    for i in range(1, n):
        if n % i == 0:
            numbers.append(i)
    
    if sum(numbers) == n:
        print("{} =".format(n), end=" ")
        for i in range(len(numbers) - 1):
            print("{} +".format(numbers[i]), end=" ")
        print(numbers[-1])
    else:
        print("{} is NOT perfect.".format(n))
