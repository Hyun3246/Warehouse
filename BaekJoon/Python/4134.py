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


N = int(sys.stdin.readline().strip())

test_case = [int(sys.stdin.readline().strip()) for i in range(N)]

prime_numbers = []

for i in test_case:
    if i <= 2:
        prime_numbers.append(2)
    else:
        while True:
            if prime_number(i):
                prime_numbers.append(i)
                break
            else:
                i += 1
                continue

for i in prime_numbers:
    print(i)
