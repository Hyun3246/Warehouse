import sys

def Eratosthenes(n):
    array = [i for i in range(n + 1)]
    end = int(n ** (1/2))
    for i in range(2, end + 1):
        if array[i] == 0:
            continue
        for j in range(i*i, n + 1, i):
            array[j] = 0
        
    return array


T = int(sys.stdin.readline().strip())

test_case = [int(sys.stdin.readline().strip()) for i in range(T)]

prime_num_list = Eratosthenes(max(test_case))

for i in test_case:
    count = 0
    
    for j in range(2, i // 2 + 1):
        if prime_num_list[j] and prime_num_list[i-j]:
            count += 1
    
    print(count)
