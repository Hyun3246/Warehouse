def ShellSort(list):
    distance = len(list) // 2
    while distance > 0:
        for i in range(distance, len(list)):
            temp = list[i]
            j = i
            # 하위 리스트 안에 든 요소들을 정렬합니다.
            while j >= distance and list[j - distance] > temp:
                list[j] = list[j - distance]
                j = j - distance
            list[j] = temp

        # 다음 패스를 위해 거리를 반으로 줄입니다.
        distance = distance // 2
    
    return list