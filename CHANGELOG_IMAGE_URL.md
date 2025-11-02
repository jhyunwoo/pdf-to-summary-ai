# 변경 로그: 이미지 입력 방식 변경 (Blob → Cloudflare R2 URL)

## 변경 날짜
2025년 11월 2일

## 변경 개요

이미지 입력 방식을 **직접 업로드(blob)** 에서 **Cloudflare R2 URL 다운로드** 방식으로 변경했습니다.

## 변경 이유

1. **효율성**: 이미지를 매번 업로드하는 대신 R2에 한 번 저장하고 URL로 참조
2. **확장성**: 대용량 이미지 처리 시 네트워크 트래픽 감소
3. **일관성**: 프론트엔드에서 R2에 업로드 후 URL만 전달하는 아키텍처와 일관성 유지
4. **캐싱**: CDN을 통한 이미지 캐싱 및 빠른 액세스 가능

## 주요 변경 사항

### 1. API 엔드포인트 변경

#### 이전 방식 (`multipart/form-data`)
```python
files = {"image": open("image.jpg", "rb")}
data = {
    "prompt": "이미지 설명",
    "temperature": 0.7,
    "max_tokens": 1000
}
response = requests.post(url, files=files, data=data)
```

#### 현재 방식 (`application/json`)
```python
payload = {
    "image_url": "https://pub-xxxxx.r2.dev/image.jpg",
    "prompt": "이미지 설명",
    "temperature": 0.7,
    "max_tokens": 1000
}
response = requests.post(url, json=payload)
```

### 2. 서버 코드 변경

**변경된 파일: `server.py`**

**이전:**
```python
@app.post("/api/generate")
async def generate_with_image(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    temperature: float = Form(0.7),
    max_tokens: int = Form(2000),
    db: Session = Depends(get_db)
):
    image_bytes = await image.read()
    # ...
```

**현재:**
```python
@app.post("/api/generate")
async def generate_with_image(
    request: ImageUrlRequest,
    db: Session = Depends(get_db)
):
    image_bytes = download_image_from_url(request.image_url)
    # ...
```

**추가된 기능:**
```python
class ImageUrlRequest(BaseModel):
    """이미지 URL로 요청하는 모델"""
    image_url: str
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000


def download_image_from_url(url: str) -> bytes:
    """URL에서 이미지를 다운로드"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 다운로드 실패: {str(e)}")
```

### 3. 데이터베이스 스키마 변경

**변경된 파일: `models.py`**

**추가된 컬럼:**
```python
image_url = Column(Text)  # 이미지 URL (Cloudflare R2 등)
```

**기존 컬럼 (레거시 지원):**
```python
image_filename = Column(String(255))  # 이미지 파일명 (있는 경우) - 레거시
```

### 4. 클라이언트 코드 변경

**변경된 파일:**
- `test_client.py`
- `example_usage.py`

**주요 변경점:**
- 파일 경로 대신 이미지 URL을 인자로 받음
- `multipart/form-data` 대신 `application/json` 요청
- 파일 읽기 코드 제거

## 마이그레이션 가이드

### 1. 데이터베이스 마이그레이션

기존 데이터베이스를 사용 중인 경우:

```bash
python migrate_add_image_url.py
```

이 스크립트는 `analysis_records` 테이블에 `image_url` 컬럼을 추가합니다.

### 2. 클라이언트 코드 업데이트

**이전 코드:**
```python
with open("image.jpg", "rb") as f:
    files = {"image": f}
    data = {"prompt": "설명", "temperature": 0.7}
    response = requests.post(url, files=files, data=data)
```

**새로운 코드:**
```python
# 먼저 이미지를 Cloudflare R2에 업로드하고 URL을 받음
image_url = upload_to_r2("image.jpg")  # 별도 구현 필요

# URL로 API 호출
payload = {
    "image_url": image_url,
    "prompt": "설명",
    "temperature": 0.7
}
response = requests.post(url, json=payload)
```

### 3. 환경 설정

추가 환경 변수 필요 없음. 이미지 URL만 공개적으로 접근 가능하면 됩니다.

## 영향을 받는 API 엔드포인트

### 변경된 엔드포인트

1. **`POST /api/generate`**
   - 요청 형식: `multipart/form-data` → `application/json`
   - 매개변수: `image: UploadFile` → `image_url: str`

2. **`POST /api/generate/stream`**
   - 요청 형식: `multipart/form-data` → `application/json`
   - 매개변수: `image: UploadFile` → `image_url: str`

### 영향 없는 엔드포인트

- `GET /` - 서버 상태 확인
- `GET /health` - 헬스체크
- `POST /api/generate/text` - 텍스트 전용 (변경 없음)
- `GET /api/records` - 분석 기록 조회
- `GET /api/records/{record_id}` - 특정 기록 조회

## 새로운 기능

1. **URL 기반 이미지 다운로드**
   - 자동으로 이미지를 다운로드하고 검증
   - 30초 타임아웃 설정
   - 에러 처리 및 상세한 오류 메시지

2. **이미지 URL 기록**
   - 데이터베이스에 이미지 URL 저장
   - 분석 이력 조회 시 원본 이미지 URL 확인 가능

## 호환성

### 하위 호환성
- ❌ 이전 API와 호환되지 않음 (요청 형식 변경)
- ✅ 데이터베이스 스키마는 하위 호환 (`image_filename` 유지)

### 상위 호환성
- ✅ 향후 다른 클라우드 스토리지(S3, GCS 등) URL도 지원 가능
- ✅ CDN URL 지원

## 테스트

### 단위 테스트
```bash
# 텍스트 전용 테스트
python test_client.py

# 이미지 URL 테스트
python test_client.py https://pub-xxxxx.r2.dev/test.jpg "설명"
```

### 예제 실행
```bash
python example_usage.py https://pub-xxxxx.r2.dev/example.jpg
```

## 알려진 제한 사항

1. **공개 URL 필요**: 이미지 URL은 인증 없이 접근 가능해야 함
2. **네트워크 의존성**: 외부 URL에 대한 네트워크 연결 필요
3. **다운로드 시간**: 큰 이미지는 다운로드 시간이 추가됨

## 향후 계획

1. **인증 지원**: 프라이빗 R2 버킷 지원 (서명된 URL)
2. **캐싱**: 자주 사용되는 이미지 로컬 캐싱
3. **배치 처리**: 여러 이미지 URL을 한 번에 처리
4. **웹훅**: 분석 완료 시 콜백 URL 호출

## 문서

새로운 사용 방법은 다음 문서를 참조하세요:
- `API_USAGE_GUIDE.md` - 상세한 API 사용 가이드
- `README.md` - 프로젝트 개요 및 시작 가이드

## 변경된 파일 목록

### 핵심 파일
- ✅ `server.py` - API 엔드포인트 변경, URL 다운로드 기능 추가
- ✅ `models.py` - `image_url` 컬럼 추가

### 클라이언트 파일
- ✅ `test_client.py` - URL 기반 테스트로 변경
- ✅ `example_usage.py` - URL 기반 예제로 변경

### 유틸리티 파일
- ✅ `migrate_add_image_url.py` - 데이터베이스 마이그레이션 스크립트 (신규)

### 문서 파일
- ✅ `API_USAGE_GUIDE.md` - API 사용 가이드 (신규)
- ✅ `CHANGELOG_IMAGE_URL.md` - 이 변경 로그 (신규)

## 롤백 방법

이전 방식으로 롤백하려면:

1. Git에서 이전 커밋으로 되돌리기
```bash
git checkout <이전_커밋_해시>
```

2. 또는 수동으로 변경 사항 되돌리기 (권장하지 않음)

## 지원

문제가 발생하면:
1. `API_USAGE_GUIDE.md`의 에러 처리 섹션 참조
2. 서버 로그 확인
3. GitHub 이슈 생성

---

**변경 담당:** AI Assistant  
**검토 필요:** 프로젝트 관리자  
**배포 준비:** ✅ 완료

