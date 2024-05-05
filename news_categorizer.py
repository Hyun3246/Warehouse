import os

# 파일 불러오기 함수
def get_file_list(dir_name):
    return os.listdir(dir_name)

# 파일 내용 분석 함수
def get_conetents(file_list):
    y_class = []        # 카테고리를 넣을 리스트
    X_text = []         # 본문을 넣을 리스트
    class_dict = {
        1: "0", 2: "0", 3:"0", 4:"0", 5:"1", 6:"1", 7:"1", 8:"1"}       # 야구는 0, 축구는 1

    for file_name in file_list:
        try:
            f = open(file_name, "r",  encoding="cp949")     # windows 형식으로 파일 인코딩해서 열기
            category = int(file_name.split(os.sep)[1].split("_")[0])    # 파일 제목 맨 앞에 있는 숫자를 출력해서 카테고리로 사용
            y_class.append(class_dict[category])        # 카테고리에 해당하는 숫자를 리스트에 넣기
            X_text.append(f.read())                     # 본문을 리스트에 넣기
            f.close()
        except UnicodeDecodeError as e:
            print(e)
            print(file_name)
    return X_text, y_class


# 정규표현식을 사용해서 불필요한 문장부호 제거
def get_cleaned_text(text):
    import re
    text = re.sub('\W+','', text.lower() )
    return text

# 단어 사전(corpus) 만들기
def get_corpus_dict(text):
    text = [sentence.split() for sentence in text]      # 문장을 잘라서 단어의 리스트로 만들기 (2차원 리스트)
    cleaned_words = [get_cleaned_text(word) for words in text for word in words]     # 불필요한 문장부호가 제거된 단어들

    from collections import OrderedDict
    corpus_dict = OrderedDict()
    for i, v in enumerate(set(cleaned_words)):       # 집합을 사용해서 중복된 단어 제거. enumerate를 사용해서 key가 단어이고 value가 인덱스인 딕셔너리 생성.
        corpus_dict[v] = i
    return corpus_dict

# 문서별로 bag of words 생성
def get_count_vector(text, corpus):         # corpus에는 get_corpus_dict에서 생성한 딕셔너리가 들어옴.
    text = [sentence.split() for sentence in text]
    word_number_list = [[corpus[get_cleaned_text(word)] for word in words] for words in text]       # 단어를 깨끗하게 만들고 단어 사전에서 해당 단어의 인덱스를 찾음. 그 인덱스를 모아서 리스트로 제작.(3차원 리스트)
    X_vector = [[0 for _ in range(len(corpus))] for x in range(len(text))]                          # 결과에 사용할 틀 제작

    for i, text in enumerate(word_number_list):     # 단어 개수를 세서 bag of words의 인덱스를 1씩 늘림.
        for word_number in text:
            X_vector[i][word_number] += 1
    return X_vector

# 문서 사이의 거리(각도) 측정
import math

# 코사인 거리 측정
def get_cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

# 유사도 점수 계산
def get_similarity_score(X_vector, source):
    source_vector = X_vector[source]
    similarity_list = []
    for target_vector in X_vector:
        similarity_list.append(
            get_cosine_similarity(source_vector, target_vector))
    return similarity_list

# 상위 n개의 유사한 뉴스 반환
def get_top_n_similarity_news(similarity_score, n):
    import operator
    x = {i:v for i, v in enumerate(similarity_score)}
    sorted_x = sorted(x.items(), key=operator.itemgetter(1))

    return list(reversed(sorted_x))[1:n+1]

# 정확도 체크(제일 처음에 분류한 카데고리 사용)
def get_accuracy(similarity_list, y_class, source_news):
    source_class = y_class[source_news]

    return sum([source_class == y_class[i[0]] for i in similarity_list]) / len(similarity_list)


if __name__ == "__main__":
    dir_name = "news_data"
    file_list = get_file_list(dir_name)
    file_list = [os.path.join(dir_name, file_name) for file_name in file_list]      # join으로 경로를 합쳐야 OS에 따른 오류가 발생하지 않음.

    X_text, y_class = get_conetents(file_list)

    corpus = get_corpus_dict(X_text)
    print("Number of words : {0}".format(len(corpus)))
    X_vector = get_count_vector(X_text, corpus)
    source_number = 10

    result = []

    for i in range(80):
        source_number = i

        similarity_score = get_similarity_score(X_vector, source_number)
        similarity_news = get_top_n_similarity_news(similarity_score, 10)
        accuracy_score = get_accuracy(similarity_news, y_class, source_number)
        result.append(accuracy_score)
    print(sum(result) / 80)
