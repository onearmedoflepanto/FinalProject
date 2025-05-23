# 📘 FinScope

**FinScope**는 실시간 주식 정보, AI 기반 댓글 분석, 커뮤니티 기능, 즐겨찾기 및 소셜 로그인을 제공하는  
**풀스택 주식 분석 플랫폼**입니다.

이 프로젝트는 **백엔드(FinScope)**와 **프론트엔드(FinScope_front)**가 **분리된 Django 프로젝트**로 구성되어 있습니다.

---

## 🛠️ 주요 기능

| 기능 | 설명 |
|------|------|
| 🔥 핫한 주식 조회 | TossInvest에서 인기 주식 크롤링 및 리스트 출력 |
| 📈 상세 정보 페이지 | 종목명, 종목코드, 가격, 등락률, 차트 이미지 제공 |
| 💬 커뮤니티 댓글 | 종목별 댓글 CRUD |
| 🤖 AI 분석 | OpenAI GPT API로 댓글 분위기 분석 + “주식 온도” 시각화 |
| ⭐ 즐겨찾기 | 관심 종목 즐겨찾기 등록 |
| 👥 팔로우 | 다른 유저 팔로우 |
| 🔐 회원 기능 | 회원가입, JWT 로그인, 마이페이지 |
| 🔗 구글 로그인 | Google OAuth2 로그인 연동 |

---

## 📂 폴더 구조

```
.
├── FinScope/          # 백엔드 (Django REST API)
└── FinScope_front/    # 프론트엔드 (정적 HTML + JS, Django 템플릿 엔진 사용)
```

---

## 🖼️ 주요 페이지

### 🔻 1. 핫한 주식 리스트 (index)
![index](./images/index.png)

### 🔻 2. 주식 상세 페이지
![detail](./images/detail.png)

### 🔻 3. 마이페이지 (회원정보 수정, 팔로우 기능 포함)
![mypage](./images/mypage.png)

### 🔻 4. 즐겨찾기한 주식
![favorites](./images/favorite.png)

### 🔻 5. 로그인 (구글 소셜 로그인 포함)
![login](./images/login.png)

---

## ⚙️ 실행 방법

### 1. 백엔드 실행 (FinScope)

```bash
cd FinScope
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  8001 # 백엔드 서버: http://127.0.0.1:8001
```

### 2. 프론트엔드 실행 (FinScope_front)

```bash
cd FinScope_front
python manage.py runserver  # 프론트 서버: http://127.0.0.1:8000
```

> 정적 페이지에서 백엔드 API(`http://127.0.0.1:8001/api/`)를 호출하는 구조입니다.

---

## 🔑 환경 변수 설정

`.env` 파일에 다음 항목을 설정해야 합니다:

```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

<details>
<summary># 🚀 FinScope v2(1.1.0) 패치노트</summary>

## 📌 주요 변경 사항
- **API 구조 리팩터링**: API 모듈화 및 코드 구조 개선
  - 모든 API 요청 및 응답 로직을 모듈화하여 유지보수성 향상
  - 백엔드 코드에서 API 로직을 분리하여 가독성 및 확장성 강화

- **프론트엔드 코드 리팩터링**
  - JS 파일 모듈화로 코드 가독성 개선
  - API 호출 로직을 전역 관리로 통합
  - 스타일링 최적화 및 불필요한 CSS 제거

- **README 업데이트**
  - 프로젝트 소개 및 주요 기능 설명 추가
  - 실행 방법 명확히 개선
  - 폴더 구조 설명 추가

## ✅ 버그 수정
- 외국 주식이 검색되지 않던 문제 수정

## 🚀 성능 개선
- API 응답 속도 최적화

## ⚡ 차기 업데이트 예정
- 사용자 개인화 추천 시스템 개선
- 소셜 로그인 보안 강화
- 다크 모드 지원
</details>

## 🧑‍💻 개발자

- **Jake Lee**  
  GitHub: [https://github.com/OneArmedofLepanto](https://github.com/yourOneArmedofLepantoname)
