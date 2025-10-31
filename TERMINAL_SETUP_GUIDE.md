# 터미널 기반 설치 및 실행 가이드

이 문서는 Docker 없이 터미널에서 직접 명령어를 입력하여 Ollama Qwen3-VL 서버를 설치하고 실행하는 방법을 설명합니다.

## 📋 목차

1. [전제 조건](#전제-조건)
2. [단계별 설치 가이드](#단계별-설치-가이드)
3. [서버 실행](#서버-실행)
4. [테스트](#테스트)
5. [서버 종료](#서버-종료)
6. [문제 해결](#문제-해결)

## 🔧 전제 조건

### 필수 소프트웨어
- **OS**: Linux (Ubuntu 20.04+) 또는 macOS
- **Python**: 3.9 이상
- **GPU**: NVIDIA GPU (선택사항, 하지만 강력 권장 - 최소 24GB VRAM)
- **CUDA**: 11.8+ (GPU 사용 시)
- **디스크**: 최소 100GB 여유 공간

### 시스템 확인

```bash
# OS 확인
uname -a

# Python 버전 확인
python3 --version

# GPU 확인 (NVIDIA GPU가 있는 경우)
nvidia-smi

# 디스크 공간 확인
df -h
```

## 🚀 단계별 설치 가이드

### 방법 1: 자동 설치 (권장)

#### 1단계: 프로젝트 디렉토리로 이동

```bash
cd /Users/jhyunwoo/projects/pdf-to-summary-ai
```

#### 2단계: 스크립트 실행 권한 부여

```bash
chmod +x setup_venv.sh setup_ollama.sh start_ollama.sh download_model.sh quick_start.sh run_server.sh stop_all.sh
```

#### 3단계: 빠른 시작 스크립트 실행

```bash
./quick_start.sh
```

이 스크립트가 자동으로 다음을 수행합니다:
- Python 가상환경 생성 및 활성화
- Python 패키지 설치
- Ollama 설치
- Ollama 서버 시작
- 모델 다운로드 (선택)

#### 4단계: 서버 실행

```bash
./run_server.sh
```

### 방법 2: 수동 설치 (단계별)

#### 1단계: Python 가상환경 설정

```bash
# 프로젝트 디렉토리로 이동
cd /Users/jhyunwoo/projects/pdf-to-summary-ai

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip setuptools wheel

# 의존성 설치
pip install -r requirements.txt

# 설치 확인
pip list
```

#### 2단계: Ollama 설치

```bash
# Ollama 설치
curl -fsSL https://ollama.com/install.sh | sh

# 설치 확인
ollama --version
```

#### 3단계: Ollama 서버 시작

```bash
# 환경 변수 설정
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=/workspace/.ollama/models

# 모델 디렉토리 생성
mkdir -p /workspace/.ollama/models

# Ollama 서버 시작 (백그라운드)
nohup ollama serve > ollama.log 2>&1 &

# 서버 시작 대기
sleep 5

# 서버 상태 확인
curl http://localhost:11434/api/tags
```

#### 4단계: Qwen3-VL 모델 다운로드

```bash
# 모델 다운로드 (약 32GB)
ollama pull qwen3-vl:32b

# 다운로드 확인
ollama list
```

**대안: 다른 크기의 모델**
```bash
# 더 작은 14B 버전
ollama pull qwen3-vl:14b

# 양자화 버전 (VRAM 절약)
ollama pull qwen3-vl:32b-q4

# 더 큰 모델 (더 많은 리소스 필요)
ollama pull qwen3-vl:235b
```

#### 5단계: API 서버 시작

```bash
# 가상환경이 활성화되어 있는지 확인
source venv/bin/activate

# 환경 변수 설정 (선택사항)
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=qwen3-vl:32b
export PORT=8000
export HOST=0.0.0.0

# 서버 시작 (포그라운드)
python server.py
```

**또는 백그라운드로 실행**:
```bash
nohup python server.py > server.log 2>&1 &

# PID 확인
echo $!

# 로그 확인
tail -f server.log
```

## 🌐 서버 실행

### 간단한 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# 서버 실행 스크립트 사용
./run_server.sh
```

### 수동 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# Ollama 서버 확인
if ! pgrep -x "ollama" > /dev/null; then
    ./start_ollama.sh
fi

# API 서버 시작
python server.py
```

### 포트 변경

```bash
# 다른 포트로 실행
PORT=8080 python server.py
```

## 🧪 테스트

### 1. 서버 상태 확인

```bash
# 기본 상태 확인
curl http://localhost:8000/

# 헬스체크
curl http://localhost:8000/health
```

### 2. 텍스트 처리 테스트

```bash
curl -X POST "http://localhost:8000/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "인공지능이란 무엇인가요?",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

### 3. 이미지 처리 테스트

```bash
# 이미지 파일 준비
# test.jpg 파일이 현재 디렉토리에 있다고 가정

curl -X POST "http://localhost:8000/api/generate" \
  -F "image=@test.jpg" \
  -F "prompt=이 이미지에 무엇이 있나요?" \
  -F "temperature=0.7" \
  -F "max_tokens=1000"
```

### 4. Python 테스트 클라이언트

```bash
# 가상환경 활성화
source venv/bin/activate

# 테스트 실행
python test_client.py

# 이미지와 함께 테스트
python test_client.py test.jpg "이 이미지를 설명해주세요"
```

### 5. 예제 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# 예제 실행
python example_usage.py test.jpg
```

## 🛑 서버 종료

### 방법 1: 자동 종료 스크립트

```bash
./stop_all.sh
```

### 방법 2: 수동 종료

```bash
# API 서버 종료
pkill -f "python server.py"

# Ollama 서버 종료
pkill ollama

# 프로세스 확인
ps aux | grep -E "ollama|python server.py"
```

### 방법 3: 포그라운드 실행 중인 경우

```bash
# Ctrl+C 키를 누르면 종료됩니다
```

## 🔄 일상적인 사용 워크플로우

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

### 상태 확인

```bash
# Ollama 서버 확인
ps aux | grep ollama

# API 서버 확인
ps aux | grep "python server.py"

# 포트 확인
netstat -tulpn | grep 8000
netstat -tulpn | grep 11434

# 또는 lsof 사용
lsof -i :8000
lsof -i :11434
```

### 로그 확인

```bash
# Ollama 로그
tail -f ollama.log

# API 서버 로그 (백그라운드 실행 시)
tail -f server.log
```

## 🔍 문제 해결

### 문제 1: 가상환경이 활성화되지 않음

**증상**: `python` 명령어가 시스템 Python을 가리킴

**해결책**:
```bash
# 가상환경 활성화
source venv/bin/activate

# 확인
which python
python --version
```

### 문제 2: Ollama 서버가 시작되지 않음

**증상**: `Connection refused` 오류

**해결책**:
```bash
# 로그 확인
cat ollama.log

# Ollama 프로세스 확인
ps aux | grep ollama

# 수동으로 시작
ollama serve > ollama.log 2>&1 &

# 잠시 대기
sleep 5

# 연결 테스트
curl http://localhost:11434/api/tags
```

### 문제 3: 모델 다운로드 실패

**증상**: 다운로드 중 연결 끊김 또는 디스크 공간 부족

**해결책**:
```bash
# 디스크 공간 확인
df -h

# 불필요한 파일 삭제
rm -rf /tmp/*

# 모델 재다운로드
ollama pull qwen3-vl:32b

# 더 작은 모델 사용
ollama pull qwen3-vl:14b

# 양자화 버전 사용 (절반 크기)
ollama pull qwen3-vl:32b-q4
```

### 문제 4: API 서버 포트가 이미 사용 중

**증상**: `Address already in use` 오류

**해결책**:
```bash
# 포트 사용 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>

# 또는 다른 포트 사용
PORT=8080 python server.py
```

### 문제 5: GPU 메모리 부족

**증상**: `CUDA out of memory` 오류

**해결책**:
```bash
# GPU 사용량 확인
nvidia-smi

# 양자화 모델 사용 (VRAM 절반으로 감소)
export MODEL_NAME=qwen3-vl:32b-q4
python server.py

# 또는 더 작은 모델
export MODEL_NAME=qwen3-vl:14b
python server.py
```

### 문제 6: 패키지 설치 오류

**증상**: `pip install` 중 오류

**해결책**:
```bash
# pip 업그레이드
pip install --upgrade pip

# 캐시 클리어
pip cache purge

# 재설치
pip install -r requirements.txt

# 특정 패키지 문제 시
pip install <package_name> --force-reinstall
```

## 📊 성능 모니터링

### GPU 모니터링

```bash
# 실시간 GPU 모니터링
watch -n 1 nvidia-smi

# 또는
nvidia-smi -l 1
```

### 서버 메트릭

```bash
# CPU 및 메모리 사용량
top

# Python 프로세스만
top -p $(pgrep -f "python server.py")

# 네트워크 연결
netstat -an | grep 8000
```

### API 응답 시간 측정

```bash
# curl로 응답 시간 측정
time curl -X POST "http://localhost:8000/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "max_tokens": 100}'
```

## 🔐 환경 변수 설정

### .env 파일 생성

```bash
# .env 파일 생성
cat > .env << EOF
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODELS=/workspace/.ollama/models
MODEL_NAME=qwen3-vl:32b
PORT=8000
HOST=0.0.0.0
PYTHONUNBUFFERED=1
EOF

# .env 파일 로드
source .env
```

### 세션별 환경 변수

```bash
# 현재 세션에만 적용
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=qwen3-vl:32b
export PORT=8000

# 영구적으로 설정 (bashrc에 추가)
echo "export OLLAMA_HOST=http://localhost:11434" >> ~/.bashrc
echo "export MODEL_NAME=qwen3-vl:32b" >> ~/.bashrc
source ~/.bashrc
```

## 📝 유용한 명령어 모음

```bash
# 전체 설치 및 시작
./quick_start.sh && ./run_server.sh

# 서버만 재시작
./stop_all.sh && ./run_server.sh

# 로그 실시간 확인
tail -f ollama.log server.log

# 가상환경 재생성
rm -rf venv && ./setup_venv.sh

# 모델 목록 확인
ollama list

# 모델 삭제
ollama rm qwen3-vl:32b

# 디스크 사용량 확인
du -sh .ollama/models/*
du -sh venv/

# 프로세스 트리 확인
pstree -p | grep -E "ollama|python"

# 시스템 리소스 확인
htop
```

## 🚀 프로덕션 배포 팁

### systemd 서비스로 등록

```bash
# systemd 서비스 파일 생성
sudo tee /etc/systemd/system/ollama-api.service << EOF
[Unit]
Description=Ollama Qwen3-VL API Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/Users/jhyunwoo/projects/pdf-to-summary-ai
ExecStartPre=/bin/bash start_ollama.sh
ExecStart=/Users/jhyunwoo/projects/pdf-to-summary-ai/venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 서비스 활성화 및 시작
sudo systemctl daemon-reload
sudo systemctl enable ollama-api
sudo systemctl start ollama-api

# 상태 확인
sudo systemctl status ollama-api
```

### 역방향 프록시 (Nginx)

```bash
# Nginx 설정
sudo tee /etc/nginx/sites-available/ollama-api << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
EOF

# 설정 활성화
sudo ln -s /etc/nginx/sites-available/ollama-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🎯 다음 단계

1. **API 문서 확인**: http://localhost:8000/docs
2. **예제 실행**: `python example_usage.py test.jpg`
3. **커스텀 애플리케이션 개발**: API를 활용한 앱 개발
4. **성능 튜닝**: 모델 파라미터 조정

---

모든 설정이 완료되었습니다! 🎉

