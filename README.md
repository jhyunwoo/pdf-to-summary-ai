# PDF to Summary AI - Ollama Qwen3-VL 서버

이 프로젝트는 VESSL 환경에서 Ollama와 Qwen3-VL:235b 모델을 사용하여 이미지와 프롬프트를 처리하는 Python API 서버입니다.

## 📋 목차

- [시스템 요구사항](#시스템-요구사항)
- [설치 방법](#설치-방법)
- [VESSL 환경 설정](#vessl-환경-설정)
- [사용 방법](#사용-방법)
- [API 엔드포인트](#api-엔드포인트)
- [테스트](#테스트)
- [문제 해결](#문제-해결)

## 🖥️ 시스템 요구사항

### 필수 요구사항
- **OS**: Linux (Ubuntu 20.04+ 권장)
- **Python**: 3.9 이상
- **GPU**: NVIDIA GPU (최소 48GB VRAM 권장)
  - Qwen3-VL:235b는 매우 큰 모델로 많은 VRAM 필요
  - A100 80GB 또는 H100 GPU 권장
- **디스크 공간**: 최소 300GB 이상 (모델 크기: ~235GB)
- **메모리**: 최소 64GB RAM 권장
- **네트워크**: 모델 다운로드를 위한 안정적인 인터넷 연결

### VESSL 권장 리소스 설정
```yaml
resource:
  cluster: vessl-gcp-oregon  # 또는 사용 가능한 클러스터
  preset: gpu-l-mem  # 또는 A100/H100 사용 가능한 프리셋
```

## 📦 설치 방법

### 빠른 시작 (권장)

```bash
# 작업 디렉토리로 이동
cd /Users/jhyunwoo/projects/pdf-to-summary-ai

# 스크립트 실행 권한 부여
chmod +x *.sh

# 빠른 시작 스크립트 실행 (모든 것을 자동으로 설정)
./quick_start.sh

# 서버 실행
./run_server.sh
```

### 수동 설치

#### 1단계: Python 가상환경 설정

```bash
# 가상환경 생성 및 의존성 설치
./setup_venv.sh

# 또는 수동으로:
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2단계: Ollama 설치

```bash
# Ollama 설치
./setup_ollama.sh

# 또는 수동으로:
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

#### 3단계: Ollama 서버 시작

```bash
# Ollama 서버 시작 (백그라운드에서 실행)
./start_ollama.sh

# 서버 상태 확인
curl http://localhost:11434/api/tags

# 서버 로그 확인
tail -f ollama.log
```

#### 4단계: Qwen3-VL 모델 다운로드

```bash
# 모델 다운로드 (시간이 오래 걸림 - 약 235GB)
./download_model.sh

# 또는 직접 ollama 명령어 사용
ollama pull qwen3-vl:235b

# 설치된 모델 확인
ollama list
```

⚠️ **주의**: 모델 다운로드는 인터넷 속도에 따라 수 시간이 걸릴 수 있습니다.

#### 5단계: Python API 서버 시작

```bash
# 가상환경 활성화
source venv/bin/activate

# 서버 실행 스크립트 사용 (권장)
./run_server.sh

# 또는 직접 실행
python server.py

# 환경 변수와 함께 시작
PORT=8080 OLLAMA_HOST=http://localhost:11434 python server.py

# 백그라운드로 실행
nohup python server.py > server.log 2>&1 &
```

## 🔧 VESSL 환경 설정

### VESSL Run으로 실행하기

VESSL에서 이 프로젝트를 실행하려면 다음 단계를 따르세요:

#### 1. VESSL CLI 설치
```bash
pip install vessl
vessl configure
```

#### 2. VESSL Run 생성

`vessl.yaml` 파일 생성:

```yaml
name: ollama-qwen3vl-server
description: Ollama Qwen3-VL API Server

image: quay.io/vessl-ai/torch:2.0.1-cuda11.8-r15

resources:
  cluster: vessl-gcp-oregon
  preset: gpu-l-mem  # A100 또는 H100 권장

import:
  /code:
    git:
      url: <YOUR_GIT_REPO_URL>
      ref: main

run:
  - command: |
      set -e
      cd /code
      
      # Python 의존성 설치
      pip install -r requirements.txt
      
      # Ollama 설치
      chmod +x setup_ollama.sh start_ollama.sh download_model.sh
      ./setup_ollama.sh
      
      # Ollama 서버 시작
      ./start_ollama.sh
      
      # 모델 다운로드 (자동으로 y 입력)
      echo "y" | ./download_model.sh
      
      # API 서버 시작
      python server.py

ports:
  - name: api
    type: http
    port: 8000
  - name: ollama
    type: http
    port: 11434

workdir: /code
```

#### 3. Run 실행
```bash
vessl run create -f vessl.yaml
```

### 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama 서버 주소 |
| `MODEL_NAME` | `qwen3-vl:235b` | 사용할 모델 이름 |
| `PORT` | `8000` | API 서버 포트 |
| `HOST` | `0.0.0.0` | API 서버 호스트 |
| `OLLAMA_MODELS` | `/workspace/.ollama/models` | 모델 저장 경로 |

## 🚀 사용 방법

### 일상적인 워크플로우

```bash
# 1. 프로젝트 디렉토리로 이동
cd /Users/jhyunwoo/projects/pdf-to-summary-ai

# 2. 가상환경 활성화
source venv/bin/activate

# 3. 서버 시작
./run_server.sh

# 4. 서버 종료 (다른 터미널에서)
./stop_all.sh
```

### 서버 상태 확인

```bash
# 서버 상태 확인
curl http://localhost:8000/

# 헬스체크
curl http://localhost:8000/health

# 프로세스 확인
ps aux | grep -E "ollama|python server.py"
```

### API 문서 확인

브라우저에서 다음 주소로 접속:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API 엔드포인트

### 1. 이미지 + 프롬프트 처리

**POST** `/api/generate`

이미지와 프롬프트를 받아서 모델이 처리한 결과를 반환합니다.

**Request (multipart/form-data):**
- `image` (file): 이미지 파일
- `prompt` (string): 처리할 프롬프트
- `temperature` (float, optional): 생성 온도 (0.0-1.0, 기본값: 0.7)
- `max_tokens` (int, optional): 최대 토큰 수 (기본값: 2000)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/generate" \
  -F "image=@example.jpg" \
  -F "prompt=이 이미지에 무엇이 있나요?" \
  -F "temperature=0.7" \
  -F "max_tokens=2000"
```

**Response:**
```json
{
  "success": true,
  "response": "이미지에는 고양이가 보입니다...",
  "model": "qwen3-vl:235b",
  "prompt": "이 이미지에 무엇이 있나요?",
  "done": true,
  "total_duration": 5000000000,
  "eval_count": 150
}
```

### 2. 텍스트만 처리

**POST** `/api/generate/text`

이미지 없이 텍스트만 처리합니다.

**Request (JSON):**
```json
{
  "prompt": "한국의 수도는?",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "한국의 수도는?",
    "temperature": 0.7,
    "max_tokens": 2000
  }'
```

### 3. 스트리밍 응답

**POST** `/api/generate/stream`

실시간으로 응답을 받아볼 수 있습니다.

**Example:**
```bash
curl -X POST "http://localhost:8000/api/generate/stream" \
  -F "image=@example.jpg" \
  -F "prompt=이 이미지를 설명해주세요" \
  -F "temperature=0.7"
```

### 4. 헬스체크

**GET** `/health`

서버와 Ollama 연결 상태를 확인합니다.

## 🧪 테스트

### Python 테스트 클라이언트

```bash
# 가상환경 활성화
source venv/bin/activate

# 기본 테스트 실행
python test_client.py

# 이미지와 함께 테스트
python test_client.py test.jpg "이 이미지를 설명해주세요"

# 예제 사용법 실행
python example_usage.py test.jpg
```

### cURL 테스트

```bash
# 1. 서버 상태 확인
curl http://localhost:8000/health

# 2. 텍스트 처리 테스트
curl -X POST "http://localhost:8000/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "인공지능이란 무엇인가요?",
    "temperature": 0.7,
    "max_tokens": 500
  }'

# 3. 이미지 처리 테스트
curl -X POST "http://localhost:8000/api/generate" \
  -F "image=@test.jpg" \
  -F "prompt=이 이미지에 대해 설명해주세요" \
  -F "temperature=0.7" \
  -F "max_tokens=1000"
```

## 🛑 서버 종료

```bash
# 자동 종료 스크립트 사용
./stop_all.sh

# 또는 수동으로 종료
pkill -f "python server.py"
pkill ollama

# 프로세스 확인
ps aux | grep -E "ollama|python server.py"
```

## 🔍 문제 해결

### 가상환경 관련

```bash
# 가상환경이 활성화되지 않은 경우
source venv/bin/activate

# 가상환경 재생성
rm -rf venv
./setup_venv.sh
```

### Ollama 서버가 시작되지 않는 경우

```bash
# 로그 확인
cat ollama.log

# Ollama 프로세스 확인
ps aux | grep ollama

# 포트 사용 확인
lsof -i :11434

# 수동으로 재시작
pkill ollama
sleep 2
./start_ollama.sh
```

### 모델 다운로드 실패

```bash
# 디스크 공간 확인
df -h

# Ollama 모델 목록 확인
ollama list

# 모델 재다운로드
ollama rm qwen3-vl:235b
ollama pull qwen3-vl:235b
```

### GPU 메모리 부족

```bash
# GPU 사용량 확인
nvidia-smi

# 더 작은 모델 사용 고려
ollama pull qwen3-vl:14b  # 더 작은 버전
```

### API 서버 연결 실패

```bash
# 가상환경 활성화 확인
source venv/bin/activate

# Python 서버 로그 확인
cat server.log

# 포그라운드에서 실행하여 로그 확인
python server.py

# 포트가 사용 중인지 확인
lsof -i :8000

# 다른 포트로 시도
PORT=8080 python server.py
```

### VESSL 환경에서 디스크 공간 문제

VESSL에서는 `/workspace` 디렉토리에 영구 저장소가 마운트됩니다:

```bash
# 모델 저장 경로를 /workspace로 설정
export OLLAMA_MODELS=/workspace/.ollama/models
mkdir -p $OLLAMA_MODELS
```

## 📊 성능 최적화

### 1. GPU 메모리 최적화

```bash
# Ollama 환경 변수 설정
export OLLAMA_NUM_PARALLEL=1  # 병렬 요청 수 제한
export OLLAMA_MAX_LOADED_MODELS=1  # 로드된 모델 수 제한
```

### 2. 모델 양자화 사용

더 작은 VRAM으로 실행하려면 양자화된 모델을 사용:

```bash
# 4-bit 양자화 버전 (VRAM 사용량 감소)
ollama pull qwen3-vl:235b-q4
```

### 3. 배치 처리

여러 요청을 동시에 처리하려면 서버 워커 수를 조정:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 2
```

## 🛠️ 개발 모드

개발 중에는 자동 리로드 활성화:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 🤝 기여

이슈와 PR을 환영합니다!

## 📧 문의

질문이나 문제가 있으면 이슈를 생성해주세요.

---

**참고 링크:**
- [Ollama 공식 문서](https://github.com/ollama/ollama)
- [Qwen3-VL 모델](https://huggingface.co/Qwen)
- [VESSL 문서](https://docs.vessl.ai/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)

