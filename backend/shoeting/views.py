from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from models import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.

# AI 모델의 output 예시 (일단 string으로)
userCharacteristics ="후드티, 청바지, 노랑, 파랑"
class UserStyle2Shoe(APIView):
    def post(self, request):
        styles = Style.objects.all()
        # 1. 각 스타일에 대해 코사인 유사도 계산
        for style in styles:
            cos_sim(style.characteristics, userCharacteristics)
        # 2. 각 신발별로 유사도 합 구하기
        shoes = Shoe.objects.all()
        sim_total = {}  # 빈 dictionary
        for shoe in shoes:
            similarity_list = getSimilarityList(shoe.id)
            similarity_total = 0
            for i in range(len(similarity_list)):
                similarity_total += similarity_list[i]
            sim_total[shoe.id] = similarity_total
        # 3. 유사도 합 높은 순으로 정렬
        dict(sorted(sim_total.items(), key=lambda item: item[1]))
        # 4. 리스트 리턴 - 유사도 합 높은 것부터 리턴 리스트에 저장
        return_list = []
        return Response(return_list)





# (비교할 스타일, 유저 스타일) -> 유사도 계산
# 코사인 유사도 - 다시 확인 필요
def cos_sim(a, b):
    vectorizer = TfidfVectorizer()
    tfidf_matrix_a = vectorizer.fit_transform(a)
    tfidf_matrix_b = vectorizer.fit_transform(b)
    cosine_sim = cosine_similarity(tfidf_matrix_a, tfidf_matrix_b)
    return cosine_sim


# 실행하면 스타일들의 유사도 리스트 - 인덱스는 style id
def getSimilarityList():
    similarity_list = []
    return similarity_list


# def colorTransfer(list):

# 자카드 유사도
# def calculateSimilarity(list1, list2):
#     s1 = set(list1)
#     s2 = set(list2)
#     return float(len(s1.intersection(s2)) / len(s1.union(s2)))
