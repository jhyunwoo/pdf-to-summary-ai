# Integer Overflow 문제 해결 가이드

## 🔴 문제 상황

서버에서 다음과 같은 에러가 발생합니다:

```
psycopg2.errors.NumericValueOutOfRange: integer out of range
sqlalchemy.exc.DataError: (psycopg2.errors.NumericValueOutOfRange) integer out of range
```

## 📌 원인

Ollama API가 반환하는 시간 값(`total_duration`, `load_duration`)은 **나노초(nanosecond)** 단위입니다.

예를 들어:
- `total_duration`: 4,491,458,261 (약 4.5초를 나노초로 표현)
- `load_duration`: 293,033,968 (약 0.3초를 나노초로 표현)

PostgreSQL의 `INTEGER` 타입은 **-2,147,483,648 ~ 2,147,483,647** 범위만 지원하므로, 약 2.1초 이상의 처리 시간이 발생하면 overflow가 발생합니다.

## ✅ 해결 방법

### 1단계: 모델 파일 확인

`models.py`가 이미 업데이트되었는지 확인:

```python
# ✅ 정상 (BigInteger 사용)
total_duration = Column(BigInteger)  # 총 처리 시간 (나노초)
load_duration = Column(BigInteger)  # 모델 로드 시간 (나노초)

# ❌ 문제 (Integer 사용)
total_duration = Column(Integer)  # 총 처리 시간 (나노초)
load_duration = Column(Integer)  # 모델 로드 시간 (나노초)
```

### 2단계: 데이터베이스 마이그레이션 실행

기존 데이터베이스의 컬럼 타입을 변경해야 합니다:

```bash
# 가상환경 활성화 (이미 되어있으면 생략)
source venv/bin/activate

# 마이그레이션 실행
python migrate_fix_integer_overflow.py
```

### 3단계: 서버 재시작

```bash
./restart_server.sh
```

또는

```bash
# 서버 중지
pkill -f "uvicorn.*server:app" || pkill -f "python.*server.py"

# 서버 시작
python server.py
```

## 📊 변경 사항 상세

### 데이터 타입 비교

| 타입 | 범위 | 최대 시간 (나노초) |
|------|------|-------------------|
| **INTEGER** | -2,147,483,648 ~ 2,147,483,647 | 약 2.1초 ❌ |
| **BIGINT** | -9,223,372,036,854,775,808 ~ 9,223,372,036,854,775,807 | 약 292년 ✅ |

### SQL 변경 내용

```sql
-- PostgreSQL
ALTER TABLE analysis_records 
ALTER COLUMN total_duration TYPE BIGINT;

ALTER TABLE analysis_records 
ALTER COLUMN load_duration TYPE BIGINT;
```

## 🧪 테스트

마이그레이션 후 API 테스트:

```bash
# 이미지 분석 테스트
python test_client.py https://your-r2-url.com/image.jpg "내용 요약해줘"
```

정상적으로 동작하면 다음과 같은 응답을 받습니다:

```json
{
  "success": true,
  "response": "...",
  "total_duration": 4491458261,
  "load_duration": 293033968,
  ...
}
```

## ⚠️ 주의사항

1. **데이터 손실 없음**: 이 마이그레이션은 기존 데이터를 유지합니다.
2. **다운타임**: 마이그레이션 중에는 서버를 재시작해야 합니다.
3. **백업 권장**: 중요한 데이터가 있다면 마이그레이션 전에 백업하세요.

## 🔍 문제 해결

### 마이그레이션 실패 시

**에러: "relation 'analysis_records' does not exist"**

```bash
# 테이블 생성 먼저 실행
python init_db.py
# 그 다음 마이그레이션
python migrate_fix_integer_overflow.py
```

**에러: "permission denied"**

- 데이터베이스 사용자에게 ALTER TABLE 권한이 있는지 확인
- PostgreSQL 관리자 계정으로 실행 필요할 수 있음

**에러: "DB_URL not found"**

```bash
# .env 파일에 DB_URL 설정
echo "DB_URL=postgresql://user:password@host:port/database" >> .env
```

## 📝 체크리스트

마이그레이션 완료 확인:

- [ ] `models.py`에 `BigInteger` import 추가됨
- [ ] `total_duration`과 `load_duration`이 `BigInteger`로 변경됨
- [ ] `migrate_fix_integer_overflow.py` 실행 완료
- [ ] 서버 재시작 완료
- [ ] API 테스트 성공

## 💡 추가 정보

### 왜 나노초를 사용하나요?

Ollama API는 정밀한 성능 측정을 위해 나노초 단위를 사용합니다:

```
1초 = 1,000,000,000 나노초
```

처리 시간이 몇 초만 넘어도 십억 단위의 숫자가 되므로 BigInteger가 필요합니다.

### 다른 컬럼은 왜 안 바꾸나요?

- `prompt_eval_count`: 토큰 수 (보통 수백~수천)
- `eval_count`: 생성된 토큰 수 (보통 수백~수천)
- `max_tokens`: 최대 토큰 수 (설정값, 보통 2000~4000)

이 값들은 Integer 범위 내에서 충분합니다.

---

**문제가 계속되면:**
- 서버 로그 확인: `tail -f server.log`
- PostgreSQL 로그 확인
- 이슈 생성 또는 문의

