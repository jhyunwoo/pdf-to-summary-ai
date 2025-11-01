# 데이터베이스 설정 가이드

## 개요

모든 API 분석 요청과 응답이 자동으로 데이터베이스에 저장됩니다. 이를 통해 분석 기록을 추적하고 관리할 수 있습니다.

## 환경 설정

### 1. .env 파일 생성

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```bash
# Database Configuration
DB_URL=sqlite:///./analysis_records.db

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=gemma3:27b

# Server Configuration
HOST=0.0.0.0
PORT=3000
```

### 2. 데이터베이스 선택

#### SQLite (기본값, 추천)
```
DB_URL=sqlite:///./analysis_records.db
```
- 별도 설치 불필요
- 단일 파일로 관리
- 소규모 프로젝트에 적합

#### PostgreSQL
```
DB_URL=postgresql://username:password@localhost:5432/pdf_summary_db
```
- 대규모 프로젝트에 적합
- 동시 접속 처리 우수

#### MySQL
```
DB_URL=mysql+pymysql://username:password@localhost:3306/pdf_summary_db
```
- 대규모 프로젝트에 적합
- 널리 사용됨

## 의존성 설치

필요한 패키지를 설치하세요:

```bash
pip install -r requirements.txt
```

또는 가상 환경이 있다면:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 서버 실행

서버를 실행하면 자동으로 데이터베이스가 초기화됩니다:

```bash
python server.py
```

또는 제공된 스크립트 사용:

```bash
./run_server.sh
```

서버 시작 시 다음과 같은 메시지가 표시됩니다:
```
✅ 데이터베이스 초기화 완료
```

## 저장되는 정보

각 API 요청마다 다음 정보가 저장됩니다:

### 요청 정보
- `endpoint`: API 엔드포인트 경로
- `prompt`: 입력 프롬프트
- `has_image`: 이미지 포함 여부
- `image_filename`: 이미지 파일명 (있는 경우)
- `temperature`: 생성 온도 설정값
- `max_tokens`: 최대 토큰 수 설정값

### 응답 정보
- `response`: 모델의 응답 텍스트
- `model`: 사용된 모델명
- `success`: 성공/실패 여부
- `error_message`: 에러 메시지 (실패 시)

### 성능 메트릭
- `total_duration`: 총 처리 시간 (나노초)
- `load_duration`: 모델 로드 시간 (나노초)
- `prompt_eval_count`: 프롬프트 평가 토큰 수
- `eval_count`: 생성된 토큰 수

### 메타데이터
- `id`: 고유 레코드 ID
- `created_at`: 생성 시각
- `updated_at`: 수정 시각

## API 엔드포인트

### 분석 기록 조회

#### 1. 전체 기록 조회
```bash
GET /api/records?skip=0&limit=100
```

**쿼리 파라미터:**
- `skip`: 건너뛸 레코드 수 (기본값: 0)
- `limit`: 가져올 최대 레코드 수 (기본값: 100)
- `endpoint`: 특정 엔드포인트로 필터링 (선택사항)

**응답 예시:**
```json
{
  "success": true,
  "total": 50,
  "records": [
    {
      "id": 1,
      "created_at": "2025-11-01T12:00:00",
      "endpoint": "/api/generate",
      "prompt": "이미지를 분석해주세요",
      "response": "이미지 분석 결과...",
      "success": true,
      ...
    }
  ]
}
```

#### 2. 특정 기록 조회
```bash
GET /api/records/{record_id}
```

**응답 예시:**
```json
{
  "success": true,
  "record": {
    "id": 1,
    "created_at": "2025-11-01T12:00:00",
    "prompt": "이미지를 분석해주세요",
    "response": "이미지 분석 결과...",
    ...
  }
}
```

#### 3. 특정 엔드포인트 기록만 조회
```bash
GET /api/records?endpoint=/api/generate/text
```

## 사용 예시

### Python으로 기록 조회하기

```python
import requests

# 전체 기록 조회
response = requests.get("http://localhost:3000/api/records")
data = response.json()
print(f"총 {data['total']}개의 기록")

# 특정 기록 조회
record_id = 1
response = requests.get(f"http://localhost:3000/api/records/{record_id}")
record = response.json()['record']
print(f"프롬프트: {record['prompt']}")
print(f"응답: {record['response']}")
```

### cURL로 기록 조회하기

```bash
# 전체 기록 조회
curl http://localhost:3000/api/records

# 특정 기록 조회
curl http://localhost:3000/api/records/1

# 텍스트 전용 엔드포인트 기록만 조회
curl "http://localhost:3000/api/records?endpoint=/api/generate/text"
```

## 데이터베이스 직접 접근

### SQLite 사용 시

```bash
# SQLite CLI로 접근
sqlite3 analysis_records.db

# 테이블 확인
.tables

# 레코드 조회
SELECT * FROM analysis_records ORDER BY created_at DESC LIMIT 10;

# 통계 조회
SELECT endpoint, COUNT(*) as count FROM analysis_records GROUP BY endpoint;
```

### PostgreSQL 사용 시

```bash
# psql로 접근
psql -U username -d pdf_summary_db

# 레코드 조회
SELECT * FROM analysis_records ORDER BY created_at DESC LIMIT 10;
```

## 데이터베이스 파일 위치

### SQLite
- 파일 경로: 프로젝트 루트의 `analysis_records.db`
- 백업: 파일을 복사하기만 하면 됩니다

### 백업 방법

```bash
# SQLite 백업
cp analysis_records.db analysis_records_backup_$(date +%Y%m%d).db

# PostgreSQL 백업
pg_dump -U username pdf_summary_db > backup_$(date +%Y%m%d).sql
```

## 문제 해결

### DB 연결 오류
- `.env` 파일의 `DB_URL`이 올바른지 확인
- PostgreSQL/MySQL 사용 시 데이터베이스 서버가 실행 중인지 확인
- 사용자 권한 확인

### 테이블이 생성되지 않음
- 서버를 재시작하면 자동으로 테이블이 생성됩니다
- 수동 생성이 필요한 경우 Python 스크립트 실행:
  ```python
  from database import init_db
  init_db()
  ```

### 기록이 저장되지 않음
- 데이터베이스 연결 확인
- 서버 로그에서 에러 메시지 확인
- 디스크 공간 확인

## 보안 고려사항

1. **민감한 정보**: 프롬프트와 응답에 민감한 정보가 포함될 수 있으므로 데이터베이스 접근을 제한하세요.

2. **.env 파일 보안**: `.env` 파일은 절대 Git에 커밋하지 마세요 (이미 .gitignore에 추가되어 있습니다).

3. **데이터베이스 암호화**: 중요한 데이터의 경우 데이터베이스 암호화를 고려하세요.

4. **접근 제한**: 프로덕션 환경에서는 `/api/records` 엔드포인트에 인증을 추가하는 것을 권장합니다.

