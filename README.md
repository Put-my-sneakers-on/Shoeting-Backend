# Shoeting-Backend
슈팅(Shoe-ting) 프로젝트의 백엔드 레포지토리입니다.

## 코드 실행 방법
### (localhost, 아직 서버에 배포되지 않음)
### git clone & install requirements
```bash
$ git clone https://github.com/Put-my-sneakers-on/Shoeting-Backend.git
$ cd Shoeting-Backend
$ pip install -r requirements.txt
```
pip install 전 가상환경 실행을 권장합니다.

### Database migration하기
1. mysql에 database를 create한다
2. manage.py와 같은 위치(Shoeting-backend/backend)에 '.env'파일을 만들고 다음과 같은 내용을 넣는다.
```python
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
DJANGO_SECRET_KEY= {시크릿 키}

DEBUG=True

DATABASE_NAME= {데이터베이스 이름}
DATABASE_USER= {데이터베이스 계정}
DATABASE_PASSWORD= {계정의 비밀번호}
DATABASE_HOST=localhost
DATABASE_PORT=3306
```
3. migration 시행  
명령어 시행 위치: Shoeting-backend/backend
```bash
$ python manage.py makemigrations shoeting
$ python manage.py migrate
```

### runserver
명령어 시행 위치: Shoeting-backend/backend
```bash
$ python manage.py runserver
```
명령어 시행 후  
http://127.0.0.1:8000/  
에 로컬서버가 켜진 것을 확인할 수 있다.

### 데이터베이스 안에 데이터 넣어보기
```bash
$ python manage.py createsuperuser
```
위 명령어를 통해 관리자계정을 생성할 수 있다.  
(명령어 시행 위치: Shoeting-backend/backend)

runserver 명령어를 시행한 상태에서 http://127.0.0.1:8000/admin 에 들어가면
django가 제공하는 관리자페이지를 이용할 수 있다.  

admin.py 파일(위치: Shoeting-backend/backend/shoeting/)에 모델들을 등록한 상태여서
관리자페이지를 통해 데이터베이스 안에 있는 데이터를 확인하고 추가, 수정, 삭제 등을 할 수 있다. 

## '스타일에 맞는 신발 추천' 기능 관련 알고리즘 test file
### 파일 위치: Shoeting-Backend/backend/
#### test_calculateSimilarity.py: 코사인 유사도 계산 함수 테스트  
style, user 변수에 비교하고 싶은 텍스트를 입력하고 파일을 실행하면 두 텍스트(style, user) 
간의 유사도 결과를 볼 수 있음 (결과는 콘솔창에 출력됨)
#### test_algorithm.py: 알고리즘 로직 테스트
마지막 줄의 ```print(test_algorithm("니트, 청바지, 채도낮음, 패턴없음"))```에서
test_algorithm 함수의 인자로 옷차림에 대한 정보를 보내면 여러 스타일과 유사도를 계산해
어울리는 순으로 신발 리스트를 리턴한다.  

실제로는 DB에서 정보를 불러오지만 아직 DB에 정보를 저장하지 않았으므로 임의의 값으로 테스트.  
자세한 내용은 해당 파일에 주석으로 설명하였다.  

## API: 추후 개발 예정
runserver 후 http://127.0.0.1:8000/shoeting 에 들어가도 연결된 api가 없는 것은 
아직 개발된 api가 없기 때문이다.