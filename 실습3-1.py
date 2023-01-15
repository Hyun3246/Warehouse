def reduce_list(my_list):
    avg = sum(my_list) / len(my_list)
    
    result = []

    for i in my_list:
        result.append((i - avg)**2)

    return result

print(reduce_list([4, 5, 8, 99, 1, 4, 7, 15]))
