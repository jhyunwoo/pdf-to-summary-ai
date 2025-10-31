# Qwen3-VL 모델 정보

이 프로젝트에서 사용하는 Qwen3-VL 모델에 대한 정보입니다.

## 현재 사용 모델: qwen3-vl:32b

### 📊 모델 사양

| 항목 | 상세 정보 |
|------|----------|
| **모델 이름** | Qwen3-VL:32b |
| **파라미터** | 32 billion |
| **모델 크기** | 약 32GB |
| **최소 VRAM** | 24GB (권장: 32GB+) |
| **최소 RAM** | 32GB (권장: 64GB) |
| **지원 언어** | 다국어 (한국어, 영어, 중국어 등) |
| **주요 기능** | Vision-Language 이해, 이미지 설명, OCR, VQA |

### 🎯 적합한 GPU

| GPU | VRAM | 적합성 | 비고 |
|-----|------|--------|------|
| RTX 3090 | 24GB | ⚠️ 최소 | 양자화 버전 권장 |
| RTX 4090 | 24GB | ⚠️ 최소 | 양자화 버전 권장 |
| RTX A5000 | 24GB | ⚠️ 최소 | 양자화 버전 권장 |
| RTX A6000 | 48GB | ✅ 권장 | 원본 모델 실행 가능 |
| A100 40GB | 40GB | ✅ 권장 | 원본 모델 실행 가능 |
| A100 80GB | 80GB | ✅✅ 최적 | 여유 있음 |
| H100 | 80GB | ✅✅ 최적 | 여유 있음 |

### 💾 디스크 공간 요구사항

- **모델 파일**: 약 32GB
- **시스템 캐시**: 약 10GB
- **로그 및 임시 파일**: 약 10GB
- **Python 가상환경**: 약 2GB
- **권장 여유 공간**: 최소 100GB

## 다른 모델 옵션

### 1. qwen3-vl:14b (더 작은 모델)

```bash
export MODEL_NAME=qwen3-vl:14b
ollama pull qwen3-vl:14b
```

**특징:**
- **크기**: 약 14GB
- **최소 VRAM**: 16GB
- **성능**: 32b보다 약간 낮지만 여전히 우수
- **속도**: 더 빠른 추론 속도

### 2. qwen3-vl:32b-q4 (양자화 버전)

```bash
export MODEL_NAME=qwen3-vl:32b-q4
ollama pull qwen3-vl:32b-q4
```

**특징:**
- **크기**: 약 16GB (절반)
- **최소 VRAM**: 16GB
- **성능**: 원본의 95% 수준
- **속도**: 비슷하거나 약간 빠름
- **장점**: VRAM이 제한적일 때 최적

### 3. qwen3-vl:235b (더 큰 모델)

```bash
export MODEL_NAME=qwen3-vl:235b
ollama pull qwen3-vl:235b
```

**특징:**
- **크기**: 약 235GB
- **최소 VRAM**: 48GB (권장: 80GB)
- **성능**: 최고 성능
- **주의**: 매우 큰 리소스 필요
- **다운로드 시간**: 수 시간 소요

## 모델 변경 방법

### 방법 1: 환경 변수 사용

```bash
# 서버 시작 시 모델 지정
export MODEL_NAME=qwen3-vl:14b
python server.py

# 또는 한 줄로
MODEL_NAME=qwen3-vl:14b python server.py
```

### 방법 2: server.py 직접 수정

```python
# server.py 파일에서 기본값 변경
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3-vl:14b")
```

### 방법 3: .env 파일 사용

```bash
# .env 파일 생성
echo "MODEL_NAME=qwen3-vl:14b" > .env

# 서버 실행
python server.py
```

## 성능 비교

| 모델 | 정확도 | 속도 | VRAM | 용도 |
|------|--------|------|------|------|
| qwen3-vl:14b | ⭐⭐⭐⭐ | 빠름 | 16GB | 개발/테스트 |
| qwen3-vl:32b | ⭐⭐⭐⭐⭐ | 보통 | 32GB | **프로덕션 권장** |
| qwen3-vl:32b-q4 | ⭐⭐⭐⭐ | 빠름 | 16GB | 리소스 제한 환경 |
| qwen3-vl:235b | ⭐⭐⭐⭐⭐+ | 느림 | 80GB | 최고 품질 필요 시 |

## 사용 시나리오별 권장

### 개발 및 테스트
- **모델**: `qwen3-vl:14b` 또는 `qwen3-vl:32b-q4`
- **이유**: 빠른 반복 개발, 리소스 절약

### 프로덕션 (일반)
- **모델**: `qwen3-vl:32b` ✅ **현재 설정**
- **이유**: 성능과 리소스의 최적 균형

### 프로덕션 (고품질)
- **모델**: `qwen3-vl:235b`
- **이유**: 최고 품질의 결과 필요

### 리소스 제한 환경
- **모델**: `qwen3-vl:32b-q4`
- **이유**: 제한된 GPU 메모리에서도 실행 가능

## 모델 다운로드 시간

인터넷 속도별 예상 다운로드 시간:

### qwen3-vl:32b (32GB)
- **100 Mbps**: 약 45분
- **1 Gbps**: 약 5분
- **10 Gbps**: 약 30초

### qwen3-vl:14b (14GB)
- **100 Mbps**: 약 20분
- **1 Gbps**: 약 2분
- **10 Gbps**: 약 15초

### qwen3-vl:235b (235GB)
- **100 Mbps**: 약 5시간
- **1 Gbps**: 약 30분
- **10 Gbps**: 약 3분

## 추가 정보

- **공식 모델 페이지**: [Qwen on Hugging Face](https://huggingface.co/Qwen)
- **Ollama 모델 라이브러리**: [Ollama Models](https://ollama.com/library/qwen3-vl)
- **모델 라이센스**: Apache 2.0 (상업적 사용 가능)

## 문제 해결

### GPU 메모리 부족
```bash
# 양자화 버전으로 전환
export MODEL_NAME=qwen3-vl:32b-q4
ollama pull qwen3-vl:32b-q4

# 또는 더 작은 모델
export MODEL_NAME=qwen3-vl:14b
ollama pull qwen3-vl:14b
```

### 느린 추론 속도
```bash
# 더 작은 모델 사용
export MODEL_NAME=qwen3-vl:14b
```

### 정확도 개선 필요
```bash
# 더 큰 모델 사용 (리소스 충분한 경우)
export MODEL_NAME=qwen3-vl:235b
ollama pull qwen3-vl:235b
```

