from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from .serializers import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Create your views here.
class JoinView(APIView):
    serializer_class = JoinSerializer

    def post(self, request):
        # 비밀번호 유효성 검사
        pw = request.data.get('password')
        regex_pw = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}'
        if not re.match(regex_pw, pw):
            return Response({"8자 이상의 영문 대/소문자, 숫자, 특수문자 조합을 입력해주세요."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "가입이 성공적으로 이루어졌습니다",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            id=request.data.get("id"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인에 성공했습니다",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response({"아이디 또는 패스워드 오류입니다."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refresh')
        return response


# AI 모델의 output 예시 (일단 string으로)
userCharacteristics ="후드티, 청바지, 노랑, 파랑"

class UserStyle2Shoe(APIView):
    def post(self, request):
        styles = Style.objects.all()
        # 1. 각 스타일에 대해 코사인 유사도 계산
        # Todo: 배열에 저장해둬야
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
        sorted_sim = sorted(sim_total.items(), key=lambda item: item[1])
        # 4. 리스트 리턴 - 유사도 합 높은 것부터 리턴 리스트에 저장 예정
        return_list = []
        for shoe_id in sorted_sim:
            return_list.append(shoe_id)
        from django.core.serializers import json
        result = json.dumps({'data': return_list})
        return HttpResponse(result, content_type ="application/json")





# (비교할 스타일, 유저 스타일) -> 유사도 계산
# 코사인 유사도
def cos_sim(a, b):
    characteristics = (a, b)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(characteristics)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
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
