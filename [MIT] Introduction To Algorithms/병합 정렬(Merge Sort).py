def MergeSort(list):
    if len(list) > 1:
        # 리스트를 반으로 나눈다.
        mid = len(list) // 2
        left = list[:mid]   # 앞 반쪽
        right = list[mid:]  # 뒤 반쪽

        # 나뉜 부분의 크기가 1이 될 때까지 반복해서 쪼갠다.
        MergeSort(left)
        MergeSort(right)

        a, b = 0, 0  # 병합(merge) 과정 종료 여부를 판단하기 위한 장치
        c = 0   # 정렬된 리스트 인덱스

        # 병합(merge) 과정
        while a < len(left) and b < len(right):
            if left[a] < right[b]:
                list[c] = left[a]
                a = a + 1
            else:
                list[c]= right[b]
                b = b + 1
            c = c + 1
        
        # left, right 어느 한 쪽에 남은 요소들을 처리해보자.
        while a < len(left):
            list[c] = left[a]
            a = a + 1
            c = c + 1
        while b < len(right):
            list[c] = right[b]
            b = b + 1
            c = c + 1
    
    return list
