def MergeSort(list):
    if len(list) > 1:
        # 리스트를 반으로 나눕니다.
        mid = len(list) // 2
        left = list[:mid]
        right = list[mid:]

        # 나뉜 부분의 크기가 1이 될 때까지 반복합니다.
        MergeSort(left)
        MergeSort(right)

        a = 0
        b = 0
        c = 0

        while a < len(left) and b < len(right):
            if left[a] < right[b]:
                list[c] = left[a]
                a = a + 1
            else:
                list[c]= right[b]
                b = b + 1
            c = c + 1
        
        while a < len(left):
            list[c] = left[a]
            a = a + 1
            c = c + 1
        while b < len(right):
            list[c] = right[b]
            b = b + 1
            c = c + 1
    
    return list