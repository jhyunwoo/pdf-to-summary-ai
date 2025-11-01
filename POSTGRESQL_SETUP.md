# PostgreSQL 설정 가이드

## PostgreSQL 설치 및 설정

### macOS에서 PostgreSQL 설치

#### 방법 1: Homebrew 사용 (추천)

```bash
# Homebrew로 PostgreSQL 설치
brew install postgresql@15

# PostgreSQL 서비스 시작
brew services start postgresql@15

# 또는 자동 시작하지 않고 수동 실행
postgres -D /opt/homebrew/var/postgresql@15
```

#### 방법 2: Postgres.app 사용

1. [Postgres.app](https://postgresapp.com/) 다운로드
2. 애플리케이션 폴더로 이동
3. Postgres.app 실행
4. "Initialize" 버튼 클릭

### 데이터베이스 및 사용자 생성

```bash
# PostgreSQL 접속
psql postgres

# 또는 특정 사용자로 접속
psql -U postgres
```

PostgreSQL 쉘에서 다음 명령어 실행:

```sql
-- 데이터베이스 생성
CREATE DATABASE pdf_summary_db;

-- 사용자 생성 (선택사항)
CREATE USER pdf_user WITH PASSWORD 'your_secure_password';

-- 사용자에게 권한 부여
GRANT ALL PRIVILEGES ON DATABASE pdf_summary_db TO pdf_user;

-- 데이터베이스 목록 확인
\l

-- 종료
\q
```

### .env 파일 설정

프로젝트의 `.env` 파일을 다음과 같이 수정하세요:

#### 기본 설정 (postgres 사용자)
```bash
DB_URL=postgresql://postgres:password@localhost:5432/pdf_summary_db
```

#### 별도 사용자 생성한 경우
```bash
DB_URL=postgresql://pdf_user:your_secure_password@localhost:5432/pdf_summary_db
```

#### 원격 서버 사용
```bash
DB_URL=postgresql://username:password@your-server.com:5432/pdf_summary_db
```

### 연결 URL 형식

```
postgresql://[사용자명]:[비밀번호]@[호스트]:[포트]/[데이터베이스명]
```

- **사용자명**: PostgreSQL 사용자 이름 (기본값: `postgres`)
- **비밀번호**: 사용자 비밀번호
- **호스트**: 서버 주소 (로컬: `localhost` 또는 `127.0.0.1`)
- **포트**: PostgreSQL 포트 (기본값: `5432`)
- **데이터베이스명**: 생성한 데이터베이스 이름

## 필수 패키지 설치

```bash
# 가상환경 활성화
source venv/bin/activate

# PostgreSQL 드라이버 설치
pip install psycopg2-binary

# 또는 전체 패키지 설치
pip install -r requirements.txt
```

## 서버 실행

```bash
python server.py
```

서버 시작 시 다음 메시지가 표시되면 성공:
```
✅ 데이터베이스 초기화 완료
```

## 연결 확인

### Python으로 연결 테스트

```python
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_URL")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("✅ PostgreSQL 연결 성공!")
except Exception as e:
    print(f"❌ 연결 실패: {e}")
```

### psql로 직접 확인

```bash
# 데이터베이스 접속
psql -U postgres -d pdf_summary_db

# 또는 별도 사용자로
psql -U pdf_user -d pdf_summary_db

# 테이블 목록 확인
\dt

# analysis_records 테이블 확인
\d analysis_records

# 데이터 조회
SELECT * FROM analysis_records ORDER BY created_at DESC LIMIT 10;

# 통계 조회
SELECT endpoint, COUNT(*) as count, 
       AVG(total_duration) as avg_duration
FROM analysis_records 
WHERE success = true
GROUP BY endpoint;
```

## 자주 발생하는 문제 해결

### 1. 연결 거부 오류
```
could not connect to server: Connection refused
```

**해결 방법:**
```bash
# PostgreSQL 서비스 상태 확인
brew services list

# PostgreSQL 시작
brew services start postgresql@15
```

### 2. 인증 실패
```
FATAL: password authentication failed for user "postgres"
```

**해결 방법:**
```bash
# 비밀번호 재설정
psql postgres
ALTER USER postgres WITH PASSWORD 'new_password';
\q
```

### 3. 데이터베이스가 존재하지 않음
```
FATAL: database "pdf_summary_db" does not exist
```

**해결 방법:**
```bash
# 데이터베이스 생성
createdb pdf_summary_db

# 또는 psql에서
psql postgres
CREATE DATABASE pdf_summary_db;
\q
```

### 4. 권한 오류
```
permission denied for schema public
```

**해결 방법:**
```sql
-- psql에서 실행
GRANT ALL ON SCHEMA public TO pdf_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pdf_user;
```

### 5. 포트가 이미 사용 중
```
Address already in use
```

**해결 방법:**
```bash
# 기존 PostgreSQL 프로세스 확인
ps aux | grep postgres

# 포트 사용 확인
lsof -i :5432

# 필요시 프로세스 종료
brew services stop postgresql@15
brew services start postgresql@15
```

## PostgreSQL 관리 도구

### 1. pgAdmin (GUI 도구)
```bash
# Homebrew로 설치
brew install --cask pgadmin4
```

### 2. DBeaver (범용 DB 도구)
```bash
brew install --cask dbeaver-community
```

### 3. TablePlus (macOS 전용)
```bash
brew install --cask tableplus
```

## 백업 및 복원

### 백업
```bash
# 전체 데이터베이스 백업
pg_dump -U postgres pdf_summary_db > backup_$(date +%Y%m%d).sql

# 압축 백업
pg_dump -U postgres pdf_summary_db | gzip > backup_$(date +%Y%m%d).sql.gz

# 특정 테이블만 백업
pg_dump -U postgres -t analysis_records pdf_summary_db > analysis_backup.sql
```

### 복원
```bash
# SQL 파일에서 복원
psql -U postgres pdf_summary_db < backup_20251101.sql

# 압축 파일에서 복원
gunzip -c backup_20251101.sql.gz | psql -U postgres pdf_summary_db
```

## 성능 최적화

### 인덱스 생성 (이미 자동 생성됨)
```sql
-- 생성 시간으로 조회 최적화
CREATE INDEX idx_created_at ON analysis_records(created_at DESC);

-- 엔드포인트별 조회 최적화
CREATE INDEX idx_endpoint ON analysis_records(endpoint);

-- 성공/실패 필터링 최적화
CREATE INDEX idx_success ON analysis_records(success);
```

### 통계 업데이트
```sql
-- 테이블 통계 업데이트
ANALYZE analysis_records;
```

### 테이블 정리
```sql
-- 죽은 튜플 제거 및 통계 업데이트
VACUUM ANALYZE analysis_records;
```

## 모니터링

### 현재 연결 확인
```sql
SELECT * FROM pg_stat_activity WHERE datname = 'pdf_summary_db';
```

### 데이터베이스 크기 확인
```sql
SELECT pg_size_pretty(pg_database_size('pdf_summary_db'));
```

### 테이블 크기 확인
```sql
SELECT pg_size_pretty(pg_total_relation_size('analysis_records'));
```

### 쿼리 성능 확인
```sql
EXPLAIN ANALYZE 
SELECT * FROM analysis_records 
WHERE endpoint = '/api/generate' 
ORDER BY created_at DESC 
LIMIT 10;
```

## 보안 권장사항

1. **강력한 비밀번호 사용**
   ```sql
   ALTER USER postgres WITH PASSWORD 'very_strong_password_123!@#';
   ```

2. **원격 접속 제한** (`postgresql.conf`)
   ```
   listen_addresses = 'localhost'
   ```

3. **SSL 연결 사용**
   ```
   DB_URL=postgresql://user:pass@localhost:5432/dbname?sslmode=require
   ```

4. **정기적인 백업**
   - cron 작업으로 자동 백업 설정
   - 백업 파일 암호화

5. **로그 모니터링**
   ```bash
   tail -f /opt/homebrew/var/log/postgresql@15.log
   ```

## 유용한 SQL 쿼리

### 최근 10개 요청 조회
```sql
SELECT id, endpoint, prompt, created_at, success
FROM analysis_records 
ORDER BY created_at DESC 
LIMIT 10;
```

### 엔드포인트별 통계
```sql
SELECT 
    endpoint,
    COUNT(*) as total_requests,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN NOT success THEN 1 ELSE 0 END) as failed,
    AVG(total_duration / 1000000000.0) as avg_duration_seconds
FROM analysis_records
GROUP BY endpoint;
```

### 시간대별 요청 수
```sql
SELECT 
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as requests
FROM analysis_records
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;
```

### 에러 분석
```sql
SELECT 
    error_message,
    COUNT(*) as error_count
FROM analysis_records
WHERE success = false
GROUP BY error_message
ORDER BY error_count DESC;
```

## 추가 리소스

- [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)
- [SQLAlchemy PostgreSQL 다이얼렉트](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [psycopg2 문서](https://www.psycopg.org/docs/)

