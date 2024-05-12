import sys
import itertools
from functools import reduce

def insert_operations(length, input_num, input_oper):
    ops = {
        "0": (lambda x, y: x+y),
        "1": (lambda x, y: x-y),
        "2": (lambda x, y: x*y),
        "3": (lambda x, y: int(x/y))
    }   # 연산자를 딕셔너리에 저장한다. 딕셔너리의 value는 림다 함수로, value를 호출하면 바로 계산을 진행한다.
    
    oper_permutation = []   # 연산자의 모든 permutation을 저장
    result = []     # 모든 계산 결과를 저장
    
    list(oper_permutation.extend([str(index)]*value) for index, value in enumerate(input_oper) if value > 0)    # 연산자가 존재하는 경우에 대해, 연산자의 개수만큼 연산자의 key를 리스트에 저장한다.

    permutation = [list(x) for x in set(itertools.permutations(oper_permutation))]      # 연산자의 모든 permutation을 구해준다.

    for i in permutation:
        result.append(reduce(lambda x, y: ops[i.pop()](x, y), input_num))
    
    print(str(max(result))+"\n"+str(min(result)))


N = int(sys.stdin.readline().strip())
numbers = list(map(int, sys.stdin.readline().strip().split()))
arithmetic_operator = list(map(int, sys.stdin.readline().strip().split()))

insert_operations(N, numbers, arithmetic_operator)
