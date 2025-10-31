# 모델 변경 로그

## 🔄 최종 변경: Gemma3:27b

**변경일**: 2024년 10월 31일
**현재 모델**: gemma3:27b

## 📊 변경 히스토리

### v3.0 - Gemma3:27b (현재)
- **모델**: gemma3:27b
- **타입**: Text-only (텍스트 전용)
- **크기**: 약 27GB
- **특징**:
  - Google의 Gemma 시리즈 최신 모델
  - 텍스트 처리에 최적화
  - 빠른 응답 속도
  - 한국어 및 다국어 지원
  - 이미지 처리 불가능 (텍스트 전용)

### v2.0 - Qwen3-VL:32b
- **모델**: qwen3-vl:32b
- **타입**: Vision-Language
- **크기**: 약 32GB
- **특징**:
  - 이미지와 텍스트 모두 처리 가능
  - Vision 모델이라 텍스트만으로는 응답 제한적
  - OCR, 이미지 분석 우수

### v1.0 - Qwen3-VL:235b
- **모델**: qwen3-vl:235b
- **타입**: Vision-Language
- **크기**: 약 235GB
- **특징**:
  - 매우 큰 모델
  - 최고 품질의 이미지 분석
  - 높은 리소스 요구사항

## 🎯 Gemma3:27b 선택 이유

### 장점
1. ✅ **텍스트 응답 우수**: 텍스트 전용 모델이므로 빈 응답 문제 해결
2. ✅ **빠른 속도**: Vision 모델보다 빠른 처리 속도
3. ✅ **효율적인 리소스**: 27GB로 적당한 크기
4. ✅ **범용성**: 대화, 질문답변, 요약 등 다양한 작업에 적합
5. ✅ **안정성**: Google의 검증된 모델

### 제한사항
1. ❌ **이미지 처리 불가**: 텍스트 전용 모델
2. ⚠️ **Vision 엔드포인트**: `/api/generate` (이미지) 사용 불가

## 📝 주요 변경 파일

### 핵심 파일
- ✅ `server.py` - MODEL_NAME = "gemma3:27b"
- ✅ `download_model.sh` - 모델명 및 크기 정보 업데이트
- ✅ `run_server.sh` - 기본 모델 변경
- ✅ `vessl.yaml` - 환경 변수 업데이트
- ✅ `quick_start.sh` - 모델 확인 로직 업데이트

### 문서 파일
- ✅ `README.md` - 모델 정보 및 요구사항 업데이트
- ✅ `QUICK_REFERENCE.md` - 명령어 예제 업데이트
- ✅ `SETUP_SUMMARY.md` - 설정 정보 업데이트
- ✅ `PROJECT_STRUCTURE.md` - 프로젝트 설명 업데이트

## 🚀 사용 방법

### 모델 다운로드
```bash
ollama pull gemma3:27b
```

### 서버 시작
```bash
source venv/bin/activate
./run_server.sh
```

### 테스트
```bash
curl -X POST "http://localhost:3000/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "안녕하세요, 자기소개를 해주세요",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

## 🔄 다른 모델로 변경하기

### 텍스트 전용 모델
```bash
# Llama 3.1
export MODEL_NAME=llama3.1:8b
ollama pull llama3.1:8b

# Qwen2
export MODEL_NAME=qwen2:7b
ollama pull qwen2:7b

# Mistral
export MODEL_NAME=mistral:7b
ollama pull mistral:7b
```

### Vision 모델 (이미지 처리 필요 시)
```bash
# Qwen3-VL
export MODEL_NAME=qwen3-vl:32b
ollama pull qwen3-vl:32b

# LLaVA
export MODEL_NAME=llava:13b
ollama pull llava:13b
```

## 📊 성능 비교

| 항목 | Gemma3:27b | Qwen3-VL:32b | Qwen3-VL:235b |
|------|------------|--------------|---------------|
| **타입** | Text-only | Vision-Language | Vision-Language |
| **크기** | 27GB | 32GB | 235GB |
| **텍스트 응답** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **이미지 처리** | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐+ |
| **속도** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **VRAM** | 16GB | 24GB | 48GB+ |
| **용도** | 텍스트 처리 | 이미지+텍스트 | 고급 Vision |

## ✅ 현재 설정

```yaml
모델: gemma3:27b
포트: 3000
타입: Text-only
크기: 27GB
최소 VRAM: 16GB
권장 VRAM: 24GB
```

## 🎯 권장 사용 사례

### Gemma3:27b에 적합한 작업
- ✅ 일반 대화 및 챗봇
- ✅ 질문 답변 (Q&A)
- ✅ 텍스트 요약
- ✅ 텍스트 생성 및 작성
- ✅ 코드 설명 및 분석
- ✅ 번역 작업

### Gemma3:27b에 부적합한 작업
- ❌ 이미지 분석 및 설명
- ❌ OCR (광학 문자 인식)
- ❌ Visual Q&A
- ❌ 이미지 기반 작업

**이미지 처리가 필요하다면** `qwen3-vl:32b` 또는 `llava:13b` 모델을 사용하세요.

## 📞 추가 정보

- **Gemma 공식 문서**: https://ai.google.dev/gemma
- **Ollama 모델 라이브러리**: https://ollama.com/library/gemma3
- **모델 라이센스**: Gemma Terms of Use

---

**마지막 업데이트**: 2024년 10월 31일
**현재 버전**: v3.0 (Gemma3:27b)

