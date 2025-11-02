# API 사용 가이드 (Cloudflare R2 URL 기반)

이 문서는 Cloudflare R2 URL을 사용하여 이미지를 분석하는 API의 사용 방법을 설명합니다.

## 변경 사항

기존에는 이미지 파일을 직접 업로드(multipart/form-data)하는 방식이었지만, 이제는 **Cloudflare R2에 업로드된 이미지 URL**을 전달하는 방식으로 변경되었습니다.

### 주요 변경점

1. **이미지 전송 방식 변경**
   - 이전: `multipart/form-data`로 이미지 파일 직접 업로드
   - 이후: JSON 요청으로 이미지 URL 전달

2. **데이터베이스 스키마 변경**
   - `image_url` 컬럼 추가 (이미지 URL 저장)
   - `image_filename`은 레거시 지원을 위해 유지

## API 엔드포인트

### 1. 이미지 분석 (URL 기반)

**엔드포인트:** `POST /api/generate`

**요청 형식:** `application/json`

**요청 본문:**
```json
{
  "image_url": "https://pub-xxxxx.r2.dev/your-image.jpg",
  "prompt": "이 이미지에 대해 설명해주세요.",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**응답 예시:**
```json
{
  "success": true,
  "response": "이 이미지는...",
  "model": "gemma3:27b",
  "prompt": "이 이미지에 대해 설명해주세요.",
  "done": true,
  "context": [...],
  "total_duration": 5234567890,
  "load_duration": 1234567890,
  "prompt_eval_count": 150,
  "eval_count": 500,
  "record_id": 123
}
```

### 2. 스트리밍 응답 (URL 기반)

**엔드포인트:** `POST /api/generate/stream`

**요청 형식:** `application/json`

**요청 본문:**
```json
{
  "image_url": "https://pub-xxxxx.r2.dev/your-image.jpg",
  "prompt": "이 이미지를 분석해주세요.",
  "temperature": 0.7
}
```

**응답:** NDJSON 스트리밍 형식

### 3. 텍스트 전용 분석

**엔드포인트:** `POST /api/generate/text`

**요청 형식:** `application/json`

**요청 본문:**
```json
{
  "prompt": "인공지능에 대해 설명해주세요.",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

## Python 클라이언트 예제

### 기본 이미지 분석

```python
import requests

url = "http://localhost:3000/api/generate"

payload = {
    "image_url": "https://pub-xxxxx.r2.dev/example.jpg",
    "prompt": "이 이미지에 대해 자세히 설명해주세요.",
    "temperature": 0.7,
    "max_tokens": 1000
}

response = requests.post(url, json=payload, timeout=300)

if response.status_code == 200:
    result = response.json()
    print(result['response'])
else:
    print(f"오류: {response.status_code}")
```

### 문서 OCR (텍스트 추출)

```python
import requests

url = "http://localhost:3000/api/generate"

payload = {
    "image_url": "https://pub-xxxxx.r2.dev/document.jpg",
    "prompt": "이 이미지에 있는 모든 텍스트를 정확하게 추출해주세요.",
    "temperature": 0.1,  # 정확성을 위해 낮은 온도
    "max_tokens": 2000
}

response = requests.post(url, json=payload, timeout=300)

if response.status_code == 200:
    result = response.json()
    print("추출된 텍스트:")
    print(result['response'])
```

### 스트리밍 응답

```python
import requests
import json

url = "http://localhost:3000/api/generate/stream"

payload = {
    "image_url": "https://pub-xxxxx.r2.dev/example.jpg",
    "prompt": "이 이미지를 분석해주세요.",
    "temperature": 0.7
}

response = requests.post(url, json=payload, stream=True, timeout=300)

if response.status_code == 200:
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                if "response" in data:
                    print(data["response"], end="", flush=True)
            except json.JSONDecodeError:
                pass
    print()
```

## JavaScript/TypeScript 클라이언트 예제

### 기본 이미지 분석

```typescript
const response = await fetch('http://localhost:3000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    image_url: 'https://pub-xxxxx.r2.dev/example.jpg',
    prompt: '이 이미지에 대해 설명해주세요.',
    temperature: 0.7,
    max_tokens: 1000,
  }),
});

const result = await response.json();
console.log(result.response);
```

### 스트리밍 응답

```typescript
const response = await fetch('http://localhost:3000/api/generate/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    image_url: 'https://pub-xxxxx.r2.dev/example.jpg',
    prompt: '이 이미지를 분석해주세요.',
    temperature: 0.7,
  }),
});

const reader = response.body?.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n').filter(line => line.trim());
  
  for (const line of lines) {
    try {
      const data = JSON.parse(line);
      if (data.response) {
        process.stdout.write(data.response);
      }
    } catch (e) {
      // JSON 파싱 오류 무시
    }
  }
}
```

## cURL 예제

### 기본 이미지 분석

```bash
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://pub-xxxxx.r2.dev/example.jpg",
    "prompt": "이 이미지에 대해 설명해주세요.",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### 텍스트 전용 분석

```bash
curl -X POST http://localhost:3000/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "인공지능에 대해 설명해주세요.",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

## 마이그레이션

기존 데이터베이스를 사용 중인 경우, 다음 명령으로 마이그레이션을 수행하세요:

```bash
python migrate_add_image_url.py
```

이 스크립트는 `analysis_records` 테이블에 `image_url` 컬럼을 추가합니다.

## 에러 처리

### 이미지 다운로드 실패

```json
{
  "detail": "이미지 다운로드 실패: [에러 메시지]"
}
```

**원인:**
- 잘못된 URL
- 네트워크 연결 문제
- Cloudflare R2 접근 권한 문제

**해결 방법:**
- URL이 공개적으로 접근 가능한지 확인
- Cloudflare R2 버킷의 공개 설정 확인

### 이미지 유효성 검증 실패

```json
{
  "detail": "유효하지 않은 이미지 형식입니다."
}
```

**원인:**
- 손상된 이미지 파일
- 지원하지 않는 이미지 형식

**해결 방법:**
- JPEG, PNG, GIF, WebP 등 일반적인 이미지 형식 사용
- 이미지 파일이 손상되지 않았는지 확인

## 지원하는 이미지 형식

- JPEG/JPG
- PNG
- GIF
- WebP
- BMP
- 기타 PIL(Python Imaging Library)에서 지원하는 형식

## 성능 고려사항

1. **이미지 크기**: 큰 이미지는 다운로드 및 처리 시간이 오래 걸릴 수 있습니다.
2. **타임아웃**: 기본 타임아웃은 30초(다운로드) + 300초(모델 처리)입니다.
3. **동시 요청**: 서버 리소스를 고려하여 적절한 수의 동시 요청을 유지하세요.

## 테스트 클라이언트 실행

```bash
# 텍스트 전용 테스트
python test_client.py

# 이미지 URL 포함 테스트
python test_client.py https://pub-xxxxx.r2.dev/example.jpg "이 이미지에 무엇이 있나요?"

# 예제 스크립트 실행
python example_usage.py https://pub-xxxxx.r2.dev/example.jpg
```

## 참고 사항

- 서버는 이미지를 다운로드하여 메모리에 임시로 저장합니다. 다운로드 후 로컬에 저장하지 않습니다.
- 이미지 URL은 데이터베이스에 기록되어 추후 분석 이력 조회 시 참조할 수 있습니다.
- Cloudflare R2 URL은 공개 접근이 가능해야 합니다.

