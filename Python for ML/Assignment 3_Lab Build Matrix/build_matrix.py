import numpy as np


def n_size_ndarray_creation(n, dtype=np.int):
    return np.array(range(n**2), dtype).reshape(n, n)

# print(n_size_ndarray_creation(8))

def zero_or_one_or_empty_ndarray(shape, type=0, dtype=np.int):
    if type == 0:
        X = np.zeros(shape, dtype= dtype)
    elif type == 1:
        X = np.ones(shape, dtype= dtype)
    else:
        X = np.empty(shape, dtype= dtype)
    return X

# print(zero_or_one_or_empty_ndarray(shape=(2,2), type=1))
# print(zero_or_one_or_empty_ndarray(shape=(3,3), type=99))

def change_shape_of_ndarray(X, n_row):
    return X.flatten() if n_row == 1 else X.reshape((n_row, -1))

# X = np.ones((32,32), dtype=np.int)
# print(change_shape_of_ndarray(X, 1))
# print(change_shape_of_ndarray(X, 512))


# 내가 쓴 답
# def concat_ndarray(X_1, X_2, axis):
#     if X_1.ndim != 1 or X_2.ndim != 1:
#         try:
#             X = np.concatenate((X_1, X_2), axis = axis)
#             return X
#         except:
#             return False
#     else:
#         try:
#             X = np.concatenate((X_1, X_2), axis = abs(1-axis))
#             return X
#         except:
#             return False

# 모범답안
def concat_ndarray(X_1, X_2, axis):
    try:
        if X_1.ndim == 1:
            X_1 = X_1.reshape(1, -1)
        if X_2.ndim == 1:
            X_2 = X_2.reshape(1, -1)
        return np.concatenate((X_1, X_2), axis = axis)
    except ValueError as e:
        return False

# a = np.array([[1, 2], [3, 4]])
# b = np.array([[5, 6]])
# print(concat_ndarray(a, b, 0))
# print(concat_ndarray(a, b, 1))

# a = np.array([1, 2])
# b = np.array([5, 6, 7])
# print(concat_ndarray(a, b, 1))
# print(concat_ndarray(a, b, 0))

# 내가 쓴 답
# def normalize_ndarray(X, axis=99, dtype=np.float32):
#     if axis == 0:
#         X = (X - X.mean(axis=0)) / X.std(axis=0)
#         X = X.astype(np.dtype)
#         return X
#     elif axis == 1:
#         X = X.T
#         X = (X - X.mean(axis=0)) / X.std(axis=0)
#         X = X.astype(np.dtype)
#         return X.T
#     else:
#         X = (X - X.mean())/ X.std()
#         X = X.astype(np.dtype)
#         return X

# 모범 답안
def normalize_ndarray(X, axis=99, dtype=np.float32):
    n_row, n_column = X.shape
    if axis == 99:
        x_mean = np.mean(X)
        x_std = np.std(X)
        Z = (X - x_mean) / x_std
    if axis == 0:
        x_mean = np.mean(X, 0).reshape(1, -1)
        x_std = np.std(X, 0).reshape(1, -1)
        Z = (X - x_mean) / x_std
    if axis == 1:
        x_mean = np.mean(X, 1).reshape(n_row, -1)
        x_std = np.std(X, 1).reshape(n_row, -1)
        Z = (X - x_mean) / x_std

    return Z

# X = np.arange(12, dtype=np.float32).reshape(6,2)
# print(normalize_ndarray(X))
# print(normalize_ndarray(X, 1))
# print(normalize_ndarray(X, 0))

def save_ndarray(X, filename="test.npy"):
    file_test = open(filename, "wb")
    np.save(X, file_test)


def boolean_index(X, condition):
    return np.where(eval(str("X") + condition))

# X = np.arange(32, dtype=np.float32).reshape(4, -1)
# print(boolean_index(X, "== 3"))
# X = np.arange(32, dtype=np.float32)
# print(boolean_index(X, "> 6"))


def find_nearest_value(X, target_value):
    new_X = np.abs(X - target_value)
    return X[np.argmin(new_X)]

# X = np.random.uniform(0, 1, 100)
# target_value = 0.3
# print(find_nearest_value(X, target_value))

# 내가 쓴 답
# def get_n_largest_values(X, n):
#     TH = np.sort(X)[-n]
#     X = X[X >= TH]
#     X = np.sort(X)[::-1]
#     return X

# 모범 답안
def get_n_largest_values(X, n):
    return X[np.argsort(X)[::-1]][:n]       # 정렬하고 그 인덱스 값을 반환

# X = np.random.uniform(0, 1, 100)
# print(get_n_largest_values(X, 3))
# print(get_n_largest_values(X, 5))
