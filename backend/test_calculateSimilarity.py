from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cos_sim(a, b):
    characteristics = (a, b)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(characteristics)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim


style = "후드티, 티셔츠, 청바지, 면바지"
user = "후드티, 청바지, 검정, 줄무늬"

print("코사인 유사도: ", cos_sim(style, user))


# casual = ["후드티", "티셔츠", "면바지", "청바지"]  # Style id=1
# street = ["라이더 자켓", "청바지", "검정", "비니"]  # Style id=2
# sporty = ["레깅스", "조거팬츠", "후드티", "바람막이"]  # Style id=3
# preppy = ["니트", "조끼", "테니스 스커트", "면바지"]  # Style id=4
#
# user = ["후드티", "청바지", "노랑", "파랑"]


# 자카드 유사도
# def calculateSimilarity(list1, list2):
#     s1 = set(list1)
#     s2 = set(list2)
#     return float(len(s1.intersection(s2)) / len(s1.union(s2)))

# print('자카드 유사도: ', calculateSimilarity(casual, user))
# print('자카드 유사도: ', calculateSimilarity(street, user))
# print('자카드 유사도: ', calculateSimilarity(sporty, user))
# print('자카드 유사도: ', calculateSimilarity(preppy, user))
