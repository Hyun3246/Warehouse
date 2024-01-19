def InsertionSort(list):
    for i in range(1, len(list)):
        # key 선정
        j = i - 1
        key = list[i]

        while (list[j] > key) and (j >= 0):
            list[j + 1] = list[j]
            j = j - 1
        list[j + 1] = key
    return list
