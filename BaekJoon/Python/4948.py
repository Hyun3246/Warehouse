import sys

# 임의의 양수 M이 합성수이면 √m 보다 작거나 같은 약수를 가진다.

def prime_number(n):
    counter = 2
    sqrt_n = n ** (1/2)
    while counter <= sqrt_n:
        if n % counter == 0:
            return False
            break
        counter += 1
    
    return True

test_case = []

while True:
    a = int(sys.stdin.readline().strip())
    if a != 0:
        test_case.append(a)
        continue
    else:
        break

max_input = max(test_case)

# 전략: 가장 큰 수를 기준으로 모든 소수를 구한 뒤, 각 입력 값의 위치를 계산한다.
list_prime = []

for i in range(2, 2 * max_input + 1):
    if prime_number(i):
        list_prime.append(i)

num_of_prime_numbers = []

for i in test_case:
    counter = 0
    for j in list_prime:
        if i < j <= 2*i:
            counter += 1
    num_of_prime_numbers.append(counter)

for i in num_of_prime_numbers:
    print(i)
