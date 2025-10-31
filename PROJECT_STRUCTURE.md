# 프로젝트 구조

```
pdf-to-summary-ai/
│
├── 📄 서버 파일
│   ├── server.py                  # FastAPI 기반 메인 API 서버
│   ├── test_client.py             # API 테스트 클라이언트
│   └── example_usage.py           # 사용 예제 스크립트
│
├── 🔧 설치 및 실행 스크립트
│   ├── setup_venv.sh              # Python 가상환경 설정
│   ├── setup_ollama.sh            # Ollama 설치
│   ├── start_ollama.sh            # Ollama 서버 시작
│   ├── download_model.sh          # Qwen3-VL 모델 다운로드
│   ├── quick_start.sh             # 빠른 시작 (전체 자동화)
│   ├── run_server.sh              # API 서버 실행
│   └── stop_all.sh                # 모든 서비스 종료
│
├── ☁️ VESSL 설정
│   ├── vessl.yaml                 # VESSL Run 설정 파일
│   └── VESSL_SETUP_GUIDE.md       # VESSL 환경 설정 가이드
│
├── 📚 문서
│   ├── README.md                  # 메인 README (설치 및 사용법)
│   ├── TERMINAL_SETUP_GUIDE.md    # 터미널 기반 설치 가이드
│   └── PROJECT_STRUCTURE.md       # 이 파일
│
├── 📦 의존성
│   ├── requirements.txt           # Python 패키지 목록
│   └── .gitignore                 # Git 무시 파일 목록
│
└── 📊 로그 및 데이터 (실행 시 생성)
    ├── venv/                      # Python 가상환경
    ├── ollama.log                 # Ollama 서버 로그
    ├── server.log                 # API 서버 로그
    └── .ollama/                   # Ollama 모델 저장 디렉토리
        └── models/                # 다운로드된 모델 파일들
```

## 📄 주요 파일 설명

### 서버 파일

#### `server.py`
- **역할**: FastAPI 기반 메인 API 서버
- **기능**:
  - 이미지 + 프롬프트 처리 (`/api/generate`)
  - 텍스트 전용 처리 (`/api/generate/text`)
  - 스트리밍 응답 (`/api/generate/stream`)
  - 헬스체크 (`/health`)
- **의존성**: FastAPI, uvicorn, requests, Pillow

#### `test_client.py`
- **역할**: API 서버 테스트 클라이언트
- **기능**:
  - 서버 상태 확인
  - 텍스트 처리 테스트
  - 이미지 처리 테스트
  - 스트리밍 테스트

### 설치 및 실행 스크립트

#### `setup_venv.sh`
- **역할**: Python 가상환경 생성 및 의존성 설치
- **실행**: `./setup_venv.sh`
- **동작**:
  1. Python 버전 확인 (3.9 이상)
  2. 가상환경 생성 (venv)
  3. pip 업그레이드
  4. requirements.txt 패키지 설치

#### `setup_ollama.sh`
- **역할**: Ollama 설치
- **실행**: `./setup_ollama.sh`
- **동작**:
  1. 시스템 정보 확인
  2. GPU 확인
  3. Ollama 다운로드 및 설치

#### `start_ollama.sh`
- **역할**: Ollama 서버 시작
- **실행**: `./start_ollama.sh`
- **동작**:
  1. 기존 Ollama 프로세스 확인
  2. 환경 변수 설정
  3. 백그라운드에서 Ollama 서버 시작
  4. 서버 상태 확인

#### `download_model.sh`
- **역할**: Qwen3-VL:32b 모델 다운로드
- **실행**: `./download_model.sh`
- **동작**:
  1. 디스크 공간 확인
  2. Ollama 서버 상태 확인
  3. 모델 다운로드 (32GB)
  4. 다운로드 확인

#### `quick_start.sh`
- **역할**: 전체 설치 프로세스 자동화
- **실행**: `./quick_start.sh`
- **동작**:
  1. 파일 확인
  2. Python 확인
  3. 가상환경 설정
  4. Ollama 설치
  5. 서버 시작
  6. 모델 다운로드

#### `run_server.sh`
- **역할**: API 서버 실행
- **실행**: `./run_server.sh`
- **동작**:
  1. 가상환경 활성화 확인
  2. Ollama 서버 상태 확인
  3. 모델 확인
  4. API 서버 시작 (포그라운드/백그라운드 선택 가능)

#### `stop_all.sh`
- **역할**: 모든 서비스 종료
- **실행**: `./stop_all.sh`
- **동작**:
  1. API 서버 종료
  2. Ollama 서버 종료
  3. 프로세스 확인

### 문서

#### `TERMINAL_SETUP_GUIDE.md`
- **역할**: 터미널 기반 설치 상세 가이드
- **내용**:
  - 전제 조건
  - 단계별 설치 (자동/수동)
  - 서버 실행 및 종료
  - 테스트 방법
  - 문제 해결
  - 성능 모니터링
  - 프로덕션 배포 팁

### VESSL 설정

#### `vessl.yaml`
- **역할**: VESSL Run 설정
- **포함 내용**:
  - 리소스 할당 (GPU)
  - 코드 Import 설정
  - 실행 명령어
  - 포트 노출
  - 환경 변수
  - 볼륨 마운트

#### `VESSL_SETUP_GUIDE.md`
- **역할**: VESSL 환경 설정 상세 가이드
- **내용**:
  - VESSL 환경 이해
  - 리소스 요구사항
  - 단계별 설치 가이드
  - 트러블슈팅

## 🚀 빠른 시작 순서

### 로컬 환경 (터미널)

#### 자동 설치 (권장)

```bash
# 1. 프로젝트 디렉토리로 이동
cd /Users/jhyunwoo/projects/pdf-to-summary-ai

# 2. 스크립트 실행 권한 부여
chmod +x *.sh

# 3. 빠른 시작 (모든 것을 자동으로 설정)
./quick_start.sh

# 4. 서버 실행
./run_server.sh
```

#### 수동 설치

```bash
# 1. Python 가상환경 설정
./setup_venv.sh
source venv/bin/activate

# 2. Ollama 설치
./setup_ollama.sh

# 3. Ollama 서버 시작
./start_ollama.sh

# 4. 모델 다운로드
./download_model.sh

# 5. API 서버 시작
python server.py
```

#### 테스트

```bash
# 가상환경 활성화
source venv/bin/activate

# 테스트 실행
python test_client.py
python test_client.py test.jpg "이 이미지를 설명해주세요"
python example_usage.py test.jpg
```

#### 서버 종료

```bash
./stop_all.sh
```

### VESSL 환경

```bash
# VESSL CLI 설치
pip install vessl
vessl configure

# Run 생성
vessl run create -f vessl.yaml

# 상태 확인
vessl run list
vessl run logs <run-number>

# 포트 포워딩
vessl run port-forward <run-number> 8000:8000
```

## 📡 API 엔드포인트 개요

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/` | 서버 상태 |
| GET | `/health` | 헬스체크 |
| POST | `/api/generate` | 이미지 + 프롬프트 처리 |
| POST | `/api/generate/text` | 텍스트 전용 처리 |
| POST | `/api/generate/stream` | 스트리밍 응답 |

## 🔐 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama 서버 주소 |
| `MODEL_NAME` | `qwen3-vl:32b` | 사용할 모델 |
| `PORT` | `8000` | API 서버 포트 |
| `HOST` | `0.0.0.0` | API 서버 호스트 |
| `OLLAMA_MODELS` | `/workspace/.ollama/models` | 모델 저장 경로 |

## 📊 리소스 요구사항

### 하드웨어
- **GPU**: NVIDIA GPU (최소 48GB VRAM, A100 80GB 권장)
- **RAM**: 최소 64GB
- **디스크**: 최소 300GB (모델 포함)

### 소프트웨어
- **OS**: Linux (Ubuntu 20.04+)
- **Python**: 3.9+
- **CUDA**: 11.8+
- **Docker**: 20.10+ (Docker 사용 시)

## 🔍 트러블슈팅 가이드

### 일반적인 문제

1. **Ollama 서버가 시작되지 않음**
   - 로그 확인: `cat ollama.log`
   - 재시작: `pkill ollama && ./start_ollama.sh`

2. **모델 다운로드 실패**
   - 디스크 공간 확인: `df -h`
   - 재시도: `ollama pull qwen3-vl:32b`

3. **API 서버 연결 실패**
   - 포트 확인: `netstat -tulpn | grep 8000`
   - 로그 확인: `python server.py` (포그라운드 실행)

4. **GPU 메모리 부족**
   - GPU 사용량: `nvidia-smi`
   - 더 작은 모델 사용: `qwen3-vl:14b`

## 📚 추가 문서

- **README.md**: 메인 문서 (설치, 사용법, API)
- **VESSL_SETUP_GUIDE.md**: VESSL 환경 상세 가이드
- **API 문서**: `http://localhost:8000/docs` (서버 실행 후)

## 🤝 기여

이슈와 PR을 환영합니다!

## 📄 라이센스

MIT License

