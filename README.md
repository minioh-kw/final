# 🎵 무드 기반 노래 추천 앱

기분, 활동, 템포, 언어를 입력하면 딱 맞는 플레이리스트를 추천해주는 웹 앱입니다.

## 🛠 기술 스택

| 역할 | 기술 |
|------|------|
| 프론트엔드 | Streamlit |
| 백엔드 | FastAPI |
| 컨테이너 | Docker / Docker Compose |
| 배포 | AWS EC2 |

## 📁 프로젝트 구조

```
music-rec/
├── front/
│   ├── app.py              # Streamlit 앱
│   ├── Dockerfile
│   └── requirements.txt
├── back/
│   ├── main.py             # FastAPI 서버
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🚀 실행 방법

### 로컬 실행

```bash
docker compose up --build
```

- Streamlit: http://localhost:8501
- FastAPI 문서: http://localhost:8000/docs

### EC2 실행

```bash
# EC2 인스턴스에 접속 후
git clone <your-repo-url>
cd music-rec

# Docker Compose 실행
docker compose up -d --build

# 실행 확인
docker ps
```

접속 주소:
- `http://<EC2_PUBLIC_IP>:8501` → Streamlit 앱
- `http://<EC2_PUBLIC_IP>:8000/docs` → FastAPI Swagger 문서

> ⚠️ EC2 보안 그룹에서 **8501**, **8000** 포트를 열어야 합니다.

## 🎵 추천 흐름

```
사용자 입력 (기분/활동/템포/언어)
    ↓
Streamlit (POST /recommend)
    ↓
FastAPI (규칙 기반 추천 로직)
    ↓
JSON 응답 (플레이리스트 이름 + 곡 5개)
    ↓
Streamlit 화면 출력
```

## 📡 API 명세

### POST `/recommend`

**Request Body**
```json
{
  "mood": "행복",
  "activity": "드라이브",
  "tempo": "빠름",
  "language": "한국어"
}
```

**Response**
```json
{
  "playlist_name": "🚗 창문 열고 달리는 행복한 드라이브",
  "description": "지금 이 행복한 순간을 더욱 빛나게 해줄 곡들을 모았어요 🎶",
  "genre": "업비트 팝 / 댄스팝",
  "songs": [
    {
      "title": "Dynamite",
      "artist": "BTS",
      "genre": "팝",
      "reason": "밝고 신나는 에너지로 기분을 더욱 업시켜줘요"
    }
  ]
}
```
