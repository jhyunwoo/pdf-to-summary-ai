# 설치 요약 가이드

Docker 없이 터미널에서 직접 실행하는 Ollama Qwen3-VL 서버 설정 가이드입니다.

## ⚡ 5분 빠른 시작

```bash
# 1. 프로젝트 디렉토리로 이동
cd /Users/jhyunwoo/projects/pdf-to-summary-ai

# 2. 스크립트 실행 권한 부여
chmod +x *.sh

# 3. 전체 자동 설치 실행
./quick_start.sh

# 4. 서버 실행
./run_server.sh
```

완료! 🎉 브라우저에서 http://localhost:8000/docs 접속

## 📁 프로젝트 파일 구조

```
pdf-to-summary-ai/
├── 🐍 Python 파일
│   ├── server.py              # API 서버
│   ├── test_client.py         # 테스트 클라이언트
│   └── example_usage.py       # 사용 예제
│
├── 📜 설치 스크립트
│   ├── setup_venv.sh          # 가상환경 설정
│   ├── setup_ollama.sh        # Ollama 설치
│   ├── start_ollama.sh        # Ollama 시작
│   ├── download_model.sh      # 모델 다운로드
│   ├── quick_start.sh         # 빠른 시작
│   ├── run_server.sh          # 서버 실행
│   └── stop_all.sh            # 전체 종료
│
└── 📚 문서
    ├── README.md                    # 전체 문서
    ├── TERMINAL_SETUP_GUIDE.md      # 상세 설치 가이드
    ├── VESSL_SETUP_GUIDE.md         # VESSL 가이드
    ├── PROJECT_STRUCTURE.md         # 프로젝트 구조
    ├── QUICK_REFERENCE.md           # 빠른 참조
    └── SETUP_SUMMARY.md             # 이 파일
```

## 🔄 일상적인 워크플로우

### 서버 시작
```bash
cd /Users/jhyunwoo/projects/pdf-to-summary-ai
source venv/bin/activate
./run_server.sh
```

### 서버 종료
```bash
./stop_all.sh
```

## 🧪 테스트

```bash
# 가상환경 활성화
source venv/bin/activate

# 서버 상태 확인
curl http://localhost:8000/health

# 텍스트 테스트
python test_client.py

# 이미지 테스트 (이미지 파일 있는 경우)
python test_client.py test.jpg "이미지 설명해줘"
```

## 📖 각 스크립트 설명

| 스크립트 | 설명 | 사용 시기 |
|---------|------|----------|
| `setup_venv.sh` | Python 가상환경 생성 및 패키지 설치 | 최초 설치 시 |
| `setup_ollama.sh` | Ollama 설치 | 최초 설치 시 |
| `start_ollama.sh` | Ollama 서버 시작 | 서버 시작 전 |
| `download_model.sh` | 모델 다운로드 (32GB) | 최초 1회만 |
| `quick_start.sh` | 전체 자동 설치 | 처음 설정 시 |
| `run_server.sh` | API 서버 실행 | 매번 서버 시작 시 |
| `stop_all.sh` | 모든 서비스 종료 | 서버 종료 시 |

## ⚙️ 환경 변수

필요한 경우 다음 환경 변수를 설정:

```bash
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=qwen3-vl:32b
export PORT=8000
export HOST=0.0.0.0
```

## 🔍 상태 확인 명령어

```bash
# 가상환경 확인
which python

# Ollama 서버 확인
ps aux | grep ollama
curl http://localhost:11434/api/tags

# API 서버 확인
ps aux | grep "python server.py"
curl http://localhost:8000/health

# 모델 확인
ollama list

# 포트 확인
lsof -i :8000
lsof -i :11434
```

## ⚠️ 중요 참고사항

1. **가상환경 활성화**: 모든 Python 명령어 실행 전에 `source venv/bin/activate` 필수
2. **모델 크기**: Qwen3-VL:32b는 약 32GB입니다
3. **GPU 권장**: NVIDIA GPU (최소 24GB VRAM) 권장
4. **디스크 공간**: 최소 100GB 필요

## 🆘 문제 해결

### 가상환경이 활성화되지 않음
```bash
source venv/bin/activate
```

### Ollama 서버가 시작되지 않음
```bash
cat ollama.log
pkill ollama && ./start_ollama.sh
```

### API 서버 연결 실패
```bash
source venv/bin/activate
python server.py
```

### 모든 것을 다시 시작
```bash
./stop_all.sh
./start_ollama.sh
source venv/bin/activate
./run_server.sh
```

## 📞 추가 도움말

- **전체 문서**: `README.md`
- **상세 설치**: `TERMINAL_SETUP_GUIDE.md`
- **빠른 참조**: `QUICK_REFERENCE.md`
- **VESSL 배포**: `VESSL_SETUP_GUIDE.md`

## ✅ 설치 체크리스트

- [ ] Python 3.9+ 설치됨
- [ ] 가상환경 생성됨 (`venv/` 디렉토리 존재)
- [ ] Ollama 설치됨 (`ollama --version` 작동)
- [ ] Ollama 서버 실행 중 (`ps aux | grep ollama`)
- [ ] 모델 다운로드됨 (`ollama list` 확인)
- [ ] API 서버 실행 중 (`curl http://localhost:8000/health`)
- [ ] 테스트 성공 (`python test_client.py` 정상 작동)

모든 항목이 체크되었다면 성공! 🎊

