import math
import sys

#################################################
# Operation 1: 파일 읽기
#################################################
def read_file(filename):
    """ 
    텍스트 파일을 읽고, line의 리스트를 반환
    """
    try:
        f = open(filename, 'r')
        return f.readlines()
    except IOError:
        print("Error opening or reading input file: ",filename)
        sys.exit()

#################################################
# Operation 2: line을 단어들로 쪼개기
#################################################
def get_words_from_line_list(L):
    """
    line L을 단어로 쪼개서 모든 단어의 리스트를 반환
    """

    word_list = []
    for line in L:
        words_in_line = get_words_from_string(line)
        word_list = word_list + words_in_line
    return word_list

def get_words_from_string(line):
    """
    get_words_from_line_list() 함수에서 사용하는 함수.

    주어진 입력 문자열로부터 단어들의 리스트를 반환.
    """
    word_list = []          # line의 단어 저장
    character_list = []     # 단어의 문자들을 저장
    for c in line:
        if c.isalnum():
            character_list.append(c)
        elif len(character_list)>0:
            word = "".join(character_list)
            word = word.lower()
            word_list.append(word)
            character_list = []
    if len(character_list)>0:
        word = "".join(character_list)
        word = word.lower()
        word_list.append(word)
    return word_list

##############################################
# Operation 3: 단어의 빈도수 세기
##############################################
def count_frequency(word_list):
    """
    (단어, 빈도 수)의 형식으로 리스트 반환
    """
    L = []
    for new_word in word_list:
        for entry in L:
            if new_word == entry[0]:
                entry[1] = entry[1] + 1
                break
        else:
            L.append([new_word,1])
    return L

###############################################################
# Operation 4: 단어들을 알파벳 순으로 정렬
###############################################################
def insertion_sort(A):
    """
    삽입 정렬로 단어들을 알파벳 순으로 정렬
    """
    for j in range(len(A)):
        key = A[j]
        # A[j]를 정렬된 A[0..j-1]에 삽입
        i = j-1
        while i>-1 and A[i]>key:
            A[i+1] = A[i]
            i = i-1
        A[i+1] = key
    return A
    
#############################################
## 입력 파일에 대해 단어의 빈도수 세기
#############################################
def word_frequencies_for_file(filename):
    """
    주어진 파일에 대해 알파벳 순으로 (단어, 빈도 수)의 리스트 반환
    """

    line_list = read_file(filename)
    word_list = get_words_from_line_list(line_list)
    freq_mapping = count_frequency(word_list)
    insertion_sort(freq_mapping)

    print("File",filename,":")
    print(len(line_list),"lines,")
    print(len(word_list),"words,")
    print(len(freq_mapping),"distinct words")

    return freq_mapping
    
##############################################
# Operation 4: 두 문서 사이의 각도 재기
##############################################
def inner_product(L1,L2):
    """
    두 벡터의 내적
    예시: inner_product([["and",3],["of",2],["the",5]],
                           [["and",4],["in",1],["of",1],["this",2]]) = 14.0 
    """
    sum = 0.0
    for word1, count1 in L1:
        for word2, count2 in L2:
            if word1 == word2:
                sum += count1 * count2
    return sum

def vector_angle(L1,L2):
    """
    (단어, 빈도 수) 형식으로 된 입력을 받아서
    두 벡터 사이의 각도 반환
    """
    numerator = inner_product(L1,L2)
    denominator = math.sqrt(inner_product(L1,L1)*inner_product(L2,L2))
    return math.acos(numerator/denominator)

def main():
    if len(sys.argv) != 3:
        print("Usage: docdist1.py filename_1 filename_2")
    else:
        filename_1 = sys.argv[1]
        filename_2 = sys.argv[2]
        sorted_word_list_1 = word_frequencies_for_file(filename_1)
        sorted_word_list_2 = word_frequencies_for_file(filename_2)
        distance = vector_angle(sorted_word_list_1,sorted_word_list_2)
        print("The distance between the documents is: %0.6f (radians)"%distance)

if __name__ == "__main__":
    import profile
    profile.run("main()")
