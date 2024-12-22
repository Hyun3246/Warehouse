def BubbleSort(list):
    # 리스트에 담긴 데이터를 순서대로 정렬합니다.
    lastElementIndex = len(list) - 1
    for passNo in range(lastElementIndex, 0, -1):
        for idx in range(passNo):
            if list[idx] > list[idx+1]:
                list[idx], list[idx + 1] = list[idx + 1], list[idx]
    return list
