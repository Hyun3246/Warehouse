def IntPolsearch(list, x):
    idx0 = 0
    idxn = (len(list) - 1)
    found = False

    while idx0 <= idxn and x >= list[idx0] and x <= list[idxn]:

        # 중간 지점을 확인합니다.
        mid = idx0 + int(((float(idxn - idx0) / (list[idxn] - list[idx0]))*(x-list[idx0])))

        # 검색 대상과 중간 지점의 값을 비교합니다.

        if list[mid] == x:
            found = True
            return found
        
        if list[mid] < x:
            idx0 = mid + 1
    
    return found