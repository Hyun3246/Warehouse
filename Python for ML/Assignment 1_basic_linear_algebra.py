# 코드 설명: https://github.com/TEAMLAB-Lecture/AI-python-connect/tree/master/lab_assignments/lab_1

def vector_size_check(*vector_variables):
    return all(len(vector_variables[0]) == x for x in [len(vector) for vector in vector_variables[1:]]) # all은 리스트 안의 모든 요소가 True이면 True 반환

print(vector_size_check([1,2,3], [2,3,4], [5,6,7]))
print(vector_size_check([1, 3], [2,4], [6,7]))
print(vector_size_check([1, 3, 4], [4], [6,7]))

def vector_addition(*vector_variables):
    answer = [sum(t) for t in zip(*vector_variables)]
    return answer

print(vector_addition([1, 3], [2, 4], [6, 7]))

def vector_subtraction(*vector_variables):
    if vector_size_check(*vector_variables) == False:
        raise ArithmeticError
    answer = [2 * t[0]-sum(t) for t in zip(*vector_variables)]
    return answer

print(vector_subtraction([1, 5], [10, 4], [4, 7]))

def scalar_vector_product(alpha, vector_variable):
    answer = [alpha * a for a in vector_variable]
    return answer

print (scalar_vector_product(5,[1,2,3]))   

def matrix_size_check(*matrix_variables):
# row끼리 비교해서 Truw, column끼리 비교해서 True & 길이가 같으면 길이만 담은 set의 크기가 1이 될 것
    return all([len(set(len(matrix[0]) for matrix in matrix_variables)) == 1]) and all([len(matrix_variables[0]) == len(matrix) for matrix in matrix_variables])


def is_matrix_equal(*matrix_variables):
    return all([all([len(set(row)) == 1 for row in zip(*matrix)]) for matrix in zip(*matrix_variables)])


def matrix_addition(*matrix_variables):
    if matrix_size_check(*matrix_variables) == False:
        raise ArithmeticError
    answer = [[sum(a) for a in zip(*t)] for t in zip(*matrix_variables)]
    return answer

matrix_x = [[2, 2], [2, 2]]
matrix_y = [[2, 5], [2, 1]]
matrix_z = [[2, 4], [5, 3]]

print (matrix_addition(matrix_x, matrix_y))
print (matrix_addition(matrix_x, matrix_y, matrix_z))

def matrix_subtraction(*matrix_variables):
    if matrix_size_check(*matrix_variables) == False:
        raise ArithmeticError
    answer = [[2*a[0] - sum(a) for a in zip(*t)] for t in zip(*matrix_variables)]
    return answer

matrix_x = [[2, 2], [2, 2]]
matrix_y = [[2, 5], [2, 1]]
matrix_z = [[2, 4], [5, 3]]

print (matrix_subtraction(matrix_x, matrix_y)) 
print (matrix_subtraction(matrix_x, matrix_y, matrix_z))

def matrix_transpose(matrix_variable):
    answer = [[element for element in t] for t in zip(matrix_variable)]
    return answer

matrix_w = [[2, 5], [1, 1], [2, 2]]
print(matrix_transpose(matrix_w))

def scalar_matrix_product(alpha, matrix_variable):
    answer = [[alpha*a for a in t] for t in matrix_variable]
    return answer

matrix_x = [[2, 2], [2, 2], [2, 2]]
matrix_y = [[2, 5], [2, 1]]
matrix_z = [[2, 4], [5, 3]]
matrix_w = [[2, 5], [1, 1], [2, 2]]

print(scalar_matrix_product(3, matrix_x))
print(scalar_matrix_product(2, matrix_y)) 
print(scalar_matrix_product(4, matrix_z))
print(scalar_matrix_product(3, matrix_w)) 

def is_product_availability_matrix(matrix_a, matrix_b):
    return all(len([column_vector for column_vector in zip(*matrix_a)]) == len(matrix_b))


def matrix_product(matrix_a, matrix_b):
    if is_product_availability_matrix(matrix_a, matrix_b) == False:
        raise ArithmeticError
    answer = [[sum(a*b for a, b in zip(row_a, column_b)) for column_b in zip(*matrix_b)] for row_a in matrix_a]
    return answer

matrix_x= [[2, 5], [1, 1]]
matrix_y = [[1, 1, 2], [2, 1, 1]]
matrix_z = [[2, 4], [5, 3], [1, 3]]

print(matrix_product(matrix_y, matrix_z))
print(matrix_product(matrix_z, matrix_x))
print(matrix_product(matrix_x, matrix_x))
print(matrix_product(matrix_z, matrix_w))
