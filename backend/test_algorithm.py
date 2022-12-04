# DB에 데이터 넣기 전 알고리즘 로직 테스트용 파일
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cos_sim(a, b):
    characteristics = (a, b)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(characteristics)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim


# 실행하면 스타일들의 유사도 리스트 - 인덱스는 style id
def get_similarity_list():
    similarity_list = []
    return similarity_list


# Style 속성 정의 예시
# 실제 정의는 더 확실한 기준점으로 구체적으로 할 것, 아래 정의는 테스트용으로 DB에 넣기 전 간이로 만듦
# casual = "후드티, 맨투맨, 티셔츠, 청바지, 면바지"  (id=1)
# street = "라이더자켓, 카고팬츠, 청바지, 검정"  (id=2)
# sporty = "레깅스, 조거팬츠, 바람막이, 후드티"  (id=3)
# modern = "채도낮음, 패턴없음, 셔츠, 가디건, 슬랙스, 코트"  (id=4)

# 신발 StyleMatch 예시
# 실제 매칭은 더 확실한 기준점으로 할 것, 테스트용으로 DB에 넣기 전 간이로 만든 매칭
# 별도의 테이블로 배열을 저장하는 구조이지만 리스트로 파싱된 상태로 테스트를 진행하겠다. (신발마다 어울리는 style의 id 저장)
# 이름은 편의상 알파벳으로 하겠다.
# A = [1, 2]
# B = [1, 2, 3]
# C = [1, 4]

def test_algorithm(user):
    styles = ["후드티, 맨투맨, 티셔츠, 청바지, 면바지",
              "라이더자켓, 카고팬츠, 청바지, 검정",
              "레깅스, 조거팬츠, 바람막이, 후드티",
              "채도낮음, 패턴없음, 셔츠, 가디건, 슬랙스, 코트"]
    shoes = ["A", "B", "C"]
    # 1. 각 스타일에 대해 코사인 유사도 계산
    for style in styles:
        cos_sim(style, user)
    # ToDo 여기부터 하면 됨! (밑에 아직 수정안됨)
    # 2. 각 신발별로 유사도 합 구하기
    sim_total = {}  # 빈 dictionary
    for shoe in shoes:
        similarity_list = get_similarity_list(shoe)
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
    return result


# 실제로는 색상 정보 변환 함수를 구현해 추출된 색상에 대해 채도낮음, 밝음 등의 정보를 얻어 속성 텍스트에 추가해야 하지만
# 테스트 단계에서는 편의상 바로 input 값에 넣도록 하겠다.
test_algorithm("이 안에 옷차림에 대한 정보를 넣어보세요 ex)니트, 청바지, 채도낮음, 패턴없음")
