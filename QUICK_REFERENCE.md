# 빠른 참조 가이드

## 🚀 설치 및 실행

### 최초 설치

```bash
cd /Users/jhyunwoo/projects/pdf-to-summary-ai
chmod +x *.sh
./quick_start.sh
```

### 일상적인 사용

```bash
# 서버 시작
source venv/bin/activate
./run_server.sh

# 서버 종료
./stop_all.sh
```

## 📝 주요 명령어

### 가상환경

```bash
# 활성화
source venv/bin/activate

# 비활성화
deactivate

# 재생성
rm -rf venv && ./setup_venv.sh
```

### Ollama

```bash
# 서버 시작
./start_ollama.sh

# 서버 종료
pkill ollama

# 상태 확인
ps aux | grep ollama
curl http://localhost:11434/api/tags

# 모델 목록
ollama list

# 모델 다운로드
ollama pull qwen3-vl:32b

# 모델 삭제
ollama rm qwen3-vl:32b
```

### API 서버

```bash
# 시작
./run_server.sh

# 종료
pkill -f "python server.py"

# 상태 확인
ps aux | grep "python server.py"
lsof -i :8000

# 로그 확인
tail -f server.log
```

## 🧪 테스트

```bash
source venv/bin/activate

# 기본 테스트
python test_client.py

# 이미지 테스트
python test_client.py test.jpg "이미지 설명해줘"

# 예제 실행
python example_usage.py test.jpg

# cURL 테스트
curl http://localhost:8000/health
```

## 🔍 문제 해결

```bash
# 프로세스 확인
ps aux | grep -E "ollama|python server.py"

# 포트 확인
lsof -i :8000
lsof -i :11434

# 로그 확인
cat ollama.log
cat server.log

# 모든 서비스 종료
./stop_all.sh

# 재시작
./stop_all.sh && ./run_server.sh
```

## 🌐 접속 주소

- **API 문서**: http://localhost:8000/docs
- **헬스체크**: http://localhost:8000/health
- **Ollama API**: http://localhost:11434

## 📊 환경 변수

```bash
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=qwen3-vl:32b
export PORT=8000
export HOST=0.0.0.0
```

## 📂 중요 파일 위치

- **가상환경**: `venv/`
- **모델**: `.ollama/models/`
- **로그**: `ollama.log`, `server.log`
- **설정**: `requirements.txt`, `vessl.yaml`

