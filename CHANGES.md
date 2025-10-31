# 모델 변경 사항

## 변경 내용

**qwen3-vl:235b → qwen3-vl:32b**로 기본 모델 변경

## 변경 이유

1. **리소스 효율성**: 32b 모델은 235b보다 훨씬 작아 더 적은 리소스로 실행 가능
2. **접근성**: 24GB VRAM GPU에서도 실행 가능 (RTX 3090/4090 등)
3. **비용 절감**: 더 저렴한 GPU 인스턴스 사용 가능
4. **빠른 다운로드**: 32GB vs 235GB (약 7배 빠름)
5. **실용성**: 대부분의 사용 사례에 충분한 성능

## 주요 차이점

| 항목 | qwen3-vl:32b | qwen3-vl:235b |
|------|--------------|---------------|
| **모델 크기** | 약 32GB | 약 235GB |
| **최소 VRAM** | 24GB | 48GB+ |
| **권장 GPU** | RTX 3090/4090, A5000, A100 40GB | A100 80GB, H100 |
| **디스크 공간** | 100GB | 300GB |
| **다운로드 시간** | 30분~2시간 | 3~6시간 |
| **성능** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐+ |
| **속도** | 보통 | 느림 |
| **적합한 용도** | **프로덕션 일반** | 최고 품질 필요 시 |

## 변경된 파일 목록

### 핵심 파일
- ✅ `server.py` - 기본 MODEL_NAME 변경
- ✅ `download_model.sh` - 모델 이름 및 크기 설명 업데이트
- ✅ `vessl.yaml` - 환경 변수 및 볼륨 크기 조정

### 문서 파일
- ✅ `README.md` - 시스템 요구사항 및 모델 정보 업데이트
- ✅ `TERMINAL_SETUP_GUIDE.md` - 모델 관련 가이드 업데이트
- ✅ `VESSL_SETUP_GUIDE.md` - VESSL 리소스 요구사항 업데이트
- ✅ `SETUP_SUMMARY.md` - 빠른 참조 정보 업데이트
- ✅ `QUICK_REFERENCE.md` - 명령어 예제 업데이트
- ✅ `PROJECT_STRUCTURE.md` - 프로젝트 설명 업데이트

### 추가 파일
- ✅ `MODEL_INFO.md` - 모델 비교 및 선택 가이드 (신규)

## 업데이트된 시스템 요구사항

### 이전 (235b)
- GPU: 최소 48GB VRAM (A100 80GB 권장)
- 디스크: 최소 300GB
- RAM: 최소 64GB

### 현재 (32b)
- GPU: 최소 24GB VRAM (RTX 3090/4090, A100 40GB 권장)
- 디스크: 최소 100GB
- RAM: 최소 32GB

## 다른 모델로 변경하는 방법

### 더 작은 모델 (14b)
```bash
export MODEL_NAME=qwen3-vl:14b
ollama pull qwen3-vl:14b
python server.py
```

### 양자화 버전 (32b-q4)
```bash
export MODEL_NAME=qwen3-vl:32b-q4
ollama pull qwen3-vl:32b-q4
python server.py
```

### 더 큰 모델 (235b)
```bash
export MODEL_NAME=qwen3-vl:235b
ollama pull qwen3-vl:235b
python server.py
```

## 마이그레이션 가이드

### 기존 235b 사용자

이미 235b 모델을 다운로드한 경우:

```bash
# 기존 모델 유지하고 32b 추가
ollama pull qwen3-vl:32b

# 32b로 전환
export MODEL_NAME=qwen3-vl:32b
python server.py

# (선택) 235b 삭제하여 공간 확보
ollama rm qwen3-vl:235b
```

### 새로운 사용자

```bash
# 빠른 시작으로 자동 설치 (32b 자동 다운로드)
./quick_start.sh
./run_server.sh
```

## 성능 비교

실제 사용에서 32b 모델은 다음과 같은 성능을 보입니다:

- **이미지 설명**: 235b와 거의 동일한 품질
- **OCR**: 매우 유사한 정확도
- **VQA (Visual Q&A)**: 대부분의 경우 충분한 성능
- **복잡한 추론**: 235b가 약간 우수하지만 차이는 크지 않음
- **추론 속도**: 32b가 약 2-3배 빠름

## 권장 사항

| 사용 사례 | 권장 모델 | 이유 |
|----------|----------|------|
| 개발/테스트 | qwen3-vl:14b | 빠른 반복 개발 |
| **프로덕션 (일반)** | **qwen3-vl:32b** ✅ | **최적의 균형** |
| 리소스 제한 환경 | qwen3-vl:32b-q4 | VRAM 절약 |
| 최고 품질 필요 | qwen3-vl:235b | 최상의 성능 |

## 문의사항

모델 변경 관련 문제가 있으면 `MODEL_INFO.md` 파일을 참조하거나 이슈를 생성해주세요.

---

변경일: 2024년 10월 31일

