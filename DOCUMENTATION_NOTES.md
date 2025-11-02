# 문서 업데이트 노트

## 🔄 최근 업데이트 (2025-11-02)

### 모델 관련 문서 정리

현재 프로젝트는 **Gemma3:27b** 모델을 사용합니다.

#### 업데이트된 파일
- ✅ `server.py` - 주석 업데이트
- ✅ `test_client.py` - 출력 메시지 업데이트
- ✅ `quick_start.sh` - 출력 메시지 업데이트
- ✅ `run_server.sh` - 출력 메시지 및 모델 확인 로직 업데이트
- ✅ `SETUP_SUMMARY.md` - 문서 업데이트
- ✅ `vessl.yaml` - 프로젝트 이름 및 설명 업데이트

#### 레거시 문서 (참고용)
다음 문서들은 Qwen3-VL 모델에 대한 정보를 포함하고 있으나, **현재는 사용하지 않습니다**:

- `MODEL_INFO.md` - Qwen3-VL 모델 비교 정보 (레거시)
- `MODEL_CHANGE_LOG.md` - 모델 변경 히스토리 (레거시)
- `CHANGES.md` - Qwen3-VL 모델 변경 기록 (레거시)
- `TERMINAL_SETUP_GUIDE.md` - 터미널 설정 가이드 (일부 Qwen3-VL 언급)
- `VESSL_SETUP_GUIDE.md` - VESSL 설정 가이드 (일부 Qwen3-VL 언급)

이 문서들은 과거 프로젝트에서 Qwen3-VL 모델을 사용할 때 작성된 것으로, **참고용으로만 보관**합니다.

## 📌 현재 설정

### 사용 중인 모델
```bash
MODEL_NAME=gemma3:27b
```

### 특징
- **멀티모달**: 텍스트와 이미지 모두 처리 가능
- **모델 크기**: 약 27B 파라미터
- **VRAM 요구사항**: 최소 24GB (RTX 3090/4090, A100 40GB 권장)
- **용도**: 이미지 분석, OCR, Visual Q&A

### 이미지 처리 방식
- **입력**: Cloudflare R2 URL
- **처리**: URL에서 이미지 다운로드 → base64 인코딩 → Gemma3 모델 분석
- **출력**: JSON 형식의 분석 결과

## 🔍 모델 변경 히스토리

### 2025-11-02: Gemma3:27b
- **이유**: 멀티모달 기능, 안정성, 성능
- **변경 사항**: 
  - Cloudflare R2 URL 기반 이미지 입력
  - CORS 설정 추가
  - BigInteger 타입으로 duration 컬럼 수정

### 과거: Qwen3-VL:32b/235b (레거시)
- 이전 프로젝트에서 사용
- 관련 문서는 참고용으로 보관

## 📚 관련 문서

### 현재 사용 중인 가이드
- `README.md` - 프로젝트 메인 문서
- `API_USAGE_GUIDE.md` - API 사용 방법 (Cloudflare R2 URL)
- `CLOUDFLARE_TUNNEL_GUIDE.md` - Cloudflare Tunnel 설정
- `FIX_INTEGER_OVERFLOW.md` - Integer overflow 문제 해결
- `CHANGELOG_IMAGE_URL.md` - 이미지 입력 방식 변경 로그

### 설정 가이드
- `SETUP_SUMMARY.md` - 빠른 설치 가이드
- `DB_SETUP_GUIDE.md` - 데이터베이스 설정
- `POSTGRESQL_SETUP.md` - PostgreSQL 설정

### 마이그레이션 스크립트
- `migrate_add_image_url.py` - image_url 컬럼 추가
- `migrate_fix_integer_overflow.py` - BigInteger 타입 변경

## ⚠️ 주의사항

1. **모델 다운로드**
   ```bash
   ollama pull gemma3:27b
   ```

2. **환경 변수 설정**
   ```bash
   export MODEL_NAME=gemma3:27b
   export OLLAMA_HOST=http://localhost:11434
   export PORT=3000
   ```

3. **데이터베이스 마이그레이션**
   - image_url 컬럼 추가: `python migrate_add_image_url.py`
   - BigInteger 수정: `python migrate_fix_integer_overflow.py`

## 🔮 향후 계획

- [ ] 레거시 문서 정리 또는 제거
- [ ] Gemma3 모델 최적화 가이드 작성
- [ ] 성능 벤치마크 문서 작성
- [ ] 배치 처리 기능 추가

---

**마지막 업데이트**: 2025-11-02  
**담당자**: AI Assistant

