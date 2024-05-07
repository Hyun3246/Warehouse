import sys

# 임의의 양수 M이 합성수이면 √m 보다 작거나 같은 약수를 가진다.

def prime_number(n):
    counter = 2
    sqrt_n = n ** (1/2)
    while counter <= sqrt_n:
        if i % counter == 0:
            return False
            break
        counter += 1
    
    return True


M, N = map(int, sys.stdin.readline().strip().split())

prime_numbers = []

for i in range(M, N + 1):
    if i <= 1:
        pass
    else:
        if prime_number(i):
            prime_numbers.append(i)
        else:
            i += 1


for i in prime_numbers:
    print(i)
