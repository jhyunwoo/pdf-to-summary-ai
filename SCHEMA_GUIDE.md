# 데이터베이스 스키마 적용 가이드

## 📋 테이블 구조

### analysis_records 테이블

```sql
CREATE TABLE analysis_records (
    -- 기본 필드
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    
    -- 요청 정보
    endpoint VARCHAR(100) NOT NULL,
    prompt TEXT NOT NULL,
    has_image BOOLEAN DEFAULT FALSE,
    image_filename VARCHAR(255),
    
    -- 생성 옵션
    temperature FLOAT,
    max_tokens INTEGER,
    
    -- 응답 정보
    response TEXT,
    model VARCHAR(100),
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    
    -- 성능 메트릭
    total_duration BIGINT,
    load_duration BIGINT,
    prompt_eval_count INTEGER,
    eval_count INTEGER
);

-- 인덱스
CREATE INDEX ix_analysis_records_id ON analysis_records (id);
CREATE INDEX ix_analysis_records_endpoint ON analysis_records (endpoint);
```

## 🔄 스키마 적용 방법

### 방법 1: 자동 적용 (서버 시작 시)

서버를 실행하면 자동으로 테이블이 생성됩니다:

```bash
python server.py
```

**출력:**
```
✅ 데이터베이스 초기화 완료
🚀 Ollama Gemma3 API Server 시작
```

### 방법 2: 수동 스크립트 실행

서버 실행 없이 스키마만 적용:

```bash
# 가상환경 활성화
source venv/bin/activate

# 스키마 초기화 스크립트 실행
python init_db.py
```

**기능:**
- 기존 테이블 확인
- 스키마 적용
- 테이블 구조 출력
- 레코드 수 표시

### 방법 3: Python 코드로 직접 실행

```python
from database import init_db

# 데이터베이스 초기화
init_db()
print("스키마 적용 완료!")
```

### 방법 4: PostgreSQL에서 직접 SQL 실행

```bash
# PostgreSQL 접속
psql -U postgres -d pdf_summary_db

# 수동으로 테이블 생성 (필요시)
CREATE TABLE IF NOT EXISTS analysis_records (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    endpoint VARCHAR(100) NOT NULL,
    prompt TEXT NOT NULL,
    has_image BOOLEAN DEFAULT FALSE,
    image_filename VARCHAR(255),
    temperature FLOAT,
    max_tokens INTEGER,
    response TEXT,
    model VARCHAR(100),
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    total_duration BIGINT,
    load_duration BIGINT,
    prompt_eval_count INTEGER,
    eval_count INTEGER
);

CREATE INDEX IF NOT EXISTS ix_analysis_records_id ON analysis_records (id);
CREATE INDEX IF NOT EXISTS ix_analysis_records_endpoint ON analysis_records (endpoint);
```

## 🔍 스키마 확인 방법

### PostgreSQL에서 확인

```bash
# PostgreSQL 접속
psql -U postgres -d pdf_summary_db

# 테이블 목록 확인
\dt

# 특정 테이블 스키마 확인
\d analysis_records

# 인덱스 확인
\di

# 테이블 크기 확인
\dt+
```

**출력 예시:**
```
                                    Table "public.analysis_records"
      Column         |            Type             | Collation | Nullable |      Default
---------------------+-----------------------------+-----------+----------+-------------------
 id                  | integer                     |           | not null | nextval('...')
 created_at          | timestamp with time zone    |           | not null | CURRENT_TIMESTAMP
 updated_at          | timestamp with time zone    |           |          |
 endpoint            | character varying(100)      |           | not null |
 prompt              | text                        |           | not null |
 has_image           | boolean                     |           |          | false
 ...
```

### Python으로 확인

```python
from sqlalchemy import inspect
from database import engine

inspector = inspect(engine)

# 테이블 목록
tables = inspector.get_table_names()
print("테이블:", tables)

# 컬럼 정보
columns = inspector.get_columns('analysis_records')
for col in columns:
    print(f"{col['name']}: {col['type']}")

# 인덱스 정보
indexes = inspector.get_indexes('analysis_records')
for idx in indexes:
    print(f"Index: {idx['name']} on {idx['column_names']}")
```

## 🔧 스키마 수정 (마이그레이션)

### 현재 방식: 간단한 수정

컬럼 추가/수정이 필요한 경우:

1. `models.py`에서 모델 수정
2. 서버 재시작 또는 `init_db.py` 실행

**주의:** 기존 테이블은 자동으로 변경되지 않습니다!

### 프로덕션 권장: Alembic 사용

대규모 프로젝트나 프로덕션 환경에서는 Alembic을 사용하세요:

#### 1. Alembic 설치

```bash
pip install alembic
```

#### 2. Alembic 초기화

```bash
alembic init alembic
```

#### 3. `alembic.ini` 설정

```ini
# alembic.ini
sqlalchemy.url = postgresql://postgres:password@localhost:5432/pdf_summary_db
```

#### 4. `alembic/env.py` 설정

```python
from database import Base
from models import AnalysisRecord

target_metadata = Base.metadata
```

#### 5. 마이그레이션 생성

```bash
# 자동으로 변경사항 감지
alembic revision --autogenerate -m "Initial schema"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

## 📊 스키마 검증

### 테이블 존재 확인

```sql
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'analysis_records'
);
```

### 컬럼 확인

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'analysis_records'
ORDER BY ordinal_position;
```

### 제약조건 확인

```sql
SELECT conname, contype, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'analysis_records'::regclass;
```

## 🗑️ 스키마 재생성

### 전체 테이블 삭제 후 재생성

```bash
# PostgreSQL에서
psql -U postgres -d pdf_summary_db

DROP TABLE IF EXISTS analysis_records CASCADE;
\q

# 스키마 재생성
python init_db.py
```

### 데이터 보존하면서 스키마 수정

```sql
-- 1. 백업 테이블 생성
CREATE TABLE analysis_records_backup AS 
SELECT * FROM analysis_records;

-- 2. 기존 테이블 삭제
DROP TABLE analysis_records;

-- 3. 새 스키마로 테이블 생성
-- (init_db.py 실행)

-- 4. 데이터 복원
INSERT INTO analysis_records 
SELECT * FROM analysis_records_backup;

-- 5. 백업 테이블 삭제
DROP TABLE analysis_records_backup;
```

## 🎯 빠른 참조

| 작업 | 명령어 |
|------|--------|
| 스키마 자동 적용 | `python server.py` |
| 스키마만 적용 | `python init_db.py` |
| PostgreSQL 접속 | `psql -U postgres -d pdf_summary_db` |
| 테이블 목록 | `\dt` (psql) |
| 테이블 스키마 | `\d analysis_records` (psql) |
| 테이블 삭제 | `DROP TABLE analysis_records;` |
| 데이터 백업 | `pg_dump -t analysis_records pdf_summary_db > backup.sql` |

## 🚨 주의사항

1. **운영 환경**: 직접 DROP/CREATE 하지 말고 Alembic 사용
2. **백업**: 스키마 변경 전 항상 백업
3. **다운타임**: 마이그레이션 중 서비스 중단 고려
4. **테스트**: 개발 환경에서 먼저 테스트

## 💡 유용한 쿼리

### 빈 테이블로 스키마만 복사

```sql
CREATE TABLE analysis_records_new (LIKE analysis_records INCLUDING ALL);
```

### 테이블 통계

```sql
SELECT 
    schemaname,
    tablename,
    n_live_tup as row_count,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size
FROM pg_stat_user_tables
WHERE tablename = 'analysis_records';
```

### 컬럼별 NULL 비율

```sql
SELECT 
    column_name,
    COUNT(*) as total,
    COUNT(column_name) as non_null,
    COUNT(*) - COUNT(column_name) as null_count,
    ROUND(100.0 * (COUNT(*) - COUNT(column_name)) / COUNT(*), 2) as null_percent
FROM analysis_records, 
    information_schema.columns 
WHERE table_name = 'analysis_records'
GROUP BY column_name;
```

