# DB에 데이터 넣기 전 알고리즘 로직 테스트용 파일

# Style 속성 정의 예시
# 실제 정의는 더 확실한 기준점으로 구체적으로 할 것, 아래 정의는 테스트용으로 DB에 넣기 전 간이로 만듦
# casual = "후드티, 맨투맨, 티셔츠, 청바지, 면바지"  (id=1)
# street = "라이더자켓, 카고팬츠, 청바지, 검정"  (id=2)
# sporty = "레깅스, 조거팬츠, 바람막이, 후드티"  (id=3)
# modern = "채도낮음, 패턴없음, 셔츠, 가디건, 슬랙스, 코트"  (id=4)

# 신발 StyleMatch 예시
# 실제 매칭은 더 확실한 기준점으로 할 것, 테스트용으로 DB에 넣기 전 간이로 만든 매칭
# 별도의 테이블로 배열을 저장하는 구조이지만 리스트로 파싱된 상태로 테스트를 진행하겠다. (신발마다 어울리는 style의 id 저장)
# 숫자는 shoe id
# 1 = [1, 2]
# 2 = [1, 2, 3]
# 3 = [1, 4]


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 코사인 유사도 계산
def cos_sim(a, b):
    characteristics = (a, b)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(characteristics)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim

# 실제로는 인자로 shoe_id 넘기고 StyleMatch 테이블에서 매치된 style들을 검색해 리스트로 파싱 (style.id->style.characteristics)
# 편의상 shoe 받고 바로 해당 스타일 리스트 넘김 (test file 구현을 위한 임시 코드)
def get_style_match(shoe):
    if shoe == 1:
        return ["후드티, 맨투맨, 티셔츠, 청바지, 면바지", "라이더자켓, 카고팬츠, 청바지, 검정"]
    elif shoe == 2:
        return ["후드티, 맨투맨, 티셔츠, 청바지, 면바지", "라이더자켓, 카고팬츠, 청바지, 검정", "레깅스, 조거팬츠, 바람막이, 후드티"]
    elif shoe == 3:
        return ["후드티, 맨투맨, 티셔츠, 청바지, 면바지", "채도낮음, 패턴없음, 셔츠, 가디건, 슬랙스, 코트"]


# 스타일들의 유사도 리스트 만들어줌 - 인덱스는 style id
# 실제로는 인자로 shoe_id 넘기고 StyleMatch 테이블에서 매치된 스타일들 받아오지만 여기선 편의상 리스트를 넘김
def get_similarity_list(shoe_arr, user):
    similarity_list = []
    for style in shoe_arr:
        similarity_list.append(cos_sim(style, user))
    return similarity_list


# 알고리즘 실행
def test_algorithm(user):
    shoes = [1, 2, 3]
    # 1. 각 스타일에 대해 코사인 유사도 계산 & 2. 각 신발별로 유사도 합 구하기
    sim_total = {}  # 빈 dictionary
    for shoe in shoes:
        similarity_list = get_similarity_list(get_style_match(shoe), user)
        similarity_total = 0
        for i in range(len(similarity_list)):
            similarity_total += similarity_list[i]
        sim_total[shoe] = similarity_total
    # 3. 유사도 합 높은 순으로 정렬 후 리턴
    sorted_sim = sorted(sim_total.items(), key=lambda item: item[1], reverse=True)
    return sorted_sim



# 실제로는 색상 정보 변환 함수를 구현해 추출된 색상에 대해 채도낮음, 밝음 등의 정보를 얻어 속성 텍스트에 추가해야 하지만
# 테스트 단계에서는 편의상 바로 input 값에 넣도록 하겠다.
# print(test_algorithm("이 안에 옷차림에 대한 정보를 넣어보세요 ex)니트, 청바지, 채도낮음, 패턴없음"))
print(test_algorithm("니트, 청바지, 채도낮음, 패턴없음"))