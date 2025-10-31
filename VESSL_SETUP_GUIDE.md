# VESSL 환경 설치 및 설정 가이드

이 문서는 VESSL 환경에서 Ollama와 Qwen3-VL:235b 모델을 설정하는 방법을 자세히 설명합니다.

## 📋 목차

1. [VESSL 환경 이해하기](#vessl-환경-이해하기)
2. [리소스 요구사항](#리소스-요구사항)
3. [단계별 설치 가이드](#단계별-설치-가이드)
4. [VESSL Run 설정](#vessl-run-설정)
5. [트러블슈팅](#트러블슈팅)

## 🌐 VESSL 환경 이해하기

VESSL은 머신러닝 워크플로우를 위한 클라우드 플랫폼입니다. 다음과 같은 특징이 있습니다:

- **영구 저장소**: `/workspace` 디렉토리가 영구 볼륨으로 마운트됨
- **GPU 접근**: NVIDIA GPU를 직접 사용 가능
- **포트 포워딩**: 웹 서비스를 외부에 노출 가능
- **환경 변수**: 설정을 통해 환경 변수 관리

## 💻 리소스 요구사항

### 최소 요구사항

```yaml
resources:
  cluster: vessl-gcp-oregon
  preset: gpu-l-mem  # 최소 48GB VRAM
```

### 권장 사양

```yaml
resources:
  cluster: vessl-gcp-oregon
  preset: gpu-xl-mem  # A100 80GB 또는 H100
```

### 디스크 공간

- **모델 크기**: 약 235GB (qwen3-vl:235b)
- **시스템 및 기타**: 약 50GB
- **권장 총 용량**: 최소 500GB

## 🚀 단계별 설치 가이드

### 방법 1: VESSL Web UI 사용

#### 1단계: 프로젝트 생성

1. VESSL 웹사이트 (https://vessl.ai) 로그인
2. 새 프로젝트 생성
3. 프로젝트 이름: `ollama-qwen3vl-server`

#### 2단계: Run 생성

1. "Create Run" 클릭
2. 다음 정보 입력:
   - **Name**: `ollama-qwen3vl-api-server`
   - **Image**: `quay.io/vessl-ai/torch:2.0.1-cuda11.8-r15`
   - **Cluster**: 사용 가능한 GPU 클러스터 선택
   - **Preset**: `gpu-l-mem` 또는 `gpu-xl-mem`

#### 3단계: 코드 Import 설정

**Git Repository 사용**:
```yaml
import:
  /code:
    git:
      url: https://github.com/yourusername/pdf-to-summary-ai.git
      ref: main
```

**또는 로컬 파일 업로드**:
- ZIP 파일로 압축하여 업로드

#### 4단계: 시작 스크립트 설정

```bash
#!/bin/bash
set -e

cd /code

# 의존성 설치
pip install -r requirements.txt

# 스크립트 권한 부여
chmod +x *.sh

# Ollama 설치
./setup_ollama.sh

# Ollama 서버 시작
./start_ollama.sh

# 모델 다운로드 (선택: 사전에 다운로드된 경우 제외)
echo "y" | ./download_model.sh

# API 서버 시작
python server.py
```

#### 5단계: 포트 설정

- Port 8000 (API 서버): HTTP로 노출
- Port 11434 (Ollama): 내부 통신용

#### 6단계: 환경 변수 설정

```yaml
env:
  OLLAMA_HOST: http://localhost:11434
  MODEL_NAME: qwen3-vl:235b
  PORT: 8000
  HOST: 0.0.0.0
  OLLAMA_MODELS: /workspace/.ollama/models
```

#### 7단계: 볼륨 마운트 설정

```yaml
mount:
  /workspace:
    volume:
      name: ollama-models
      size: 500Gi
```

### 방법 2: VESSL CLI 사용

#### 1단계: VESSL CLI 설치

```bash
pip install vessl
vessl configure
```

설정 시 필요한 정보:
- VESSL API Token (웹사이트에서 발급)
- Organization name
- Project name

#### 2단계: vessl.yaml 파일 사용

프로젝트에 포함된 `vessl.yaml` 파일을 사용:

```bash
# Run 생성
vessl run create -f vessl.yaml

# 또는 커스텀 설정으로 생성
vessl run create \
  --image quay.io/vessl-ai/torch:2.0.1-cuda11.8-r15 \
  --cluster vessl-gcp-oregon \
  --preset gpu-l-mem \
  --git-ref main \
  --volume ollama-models:/workspace:500Gi
```

#### 3단계: Run 상태 확인

```bash
# Run 목록 보기
vessl run list

# 특별 Run 상태 확인
vessl run read <run-number>

# 로그 확인
vessl run logs <run-number>
```

#### 4단계: 포트 포워딩

```bash
# 로컬 머신에서 VESSL Run에 접속
vessl run port-forward <run-number> 8000:8000
```

그 후 브라우저에서 `http://localhost:8000/docs` 접속

## 📝 VESSL Run 설정 파일 상세

### 전체 vessl.yaml 예제

```yaml
name: ollama-qwen3vl-server
description: Ollama Qwen3-VL Vision Language Model API Server

# 베이스 이미지
image: quay.io/vessl-ai/torch:2.0.1-cuda11.8-r15

# 리소스 할당
resources:
  cluster: vessl-gcp-oregon
  preset: gpu-xl-mem  # A100 80GB 권장

# 코드 가져오기
import:
  /code:
    git:
      url: https://github.com/yourusername/pdf-to-summary-ai.git
      ref: main

# 실행 명령어
run:
  - command: |
      set -e
      cd /code
      
      # Python 의존성
      pip install -r requirements.txt
      
      # 스크립트 권한
      chmod +x setup_ollama.sh start_ollama.sh download_model.sh
      
      # Ollama 설치
      ./setup_ollama.sh
      
      # Ollama 서버 시작
      ./start_ollama.sh
      sleep 10
      
      # 모델 다운로드
      if ! ollama list | grep -q "qwen3-vl:235b"; then
        echo "y" | ./download_model.sh
      else
        echo "Model already exists"
      fi
      
      # API 서버 시작
      python server.py

# 포트 노출
ports:
  - name: api
    type: http
    port: 8000
  - name: ollama
    type: http
    port: 11434

# 작업 디렉토리
workdir: /code

# 환경 변수
env:
  OLLAMA_HOST: http://localhost:11434
  MODEL_NAME: qwen3-vl:235b
  PORT: 8000
  HOST: 0.0.0.0
  OLLAMA_MODELS: /workspace/.ollama/models
  PYTHONUNBUFFERED: "1"

# 영구 볼륨
mount:
  /workspace:
    volume:
      name: ollama-models
      size: 500Gi

# 재시작 정책
restart: on-failure
max_retries: 3
```

## 🔧 고급 설정

### 1. 사전 다운로드된 모델 사용

모델 다운로드 시간을 줄이려면:

1. **별도의 Run에서 모델만 다운로드**:

```bash
vessl run create \
  --image quay.io/vessl-ai/torch:2.0.1-cuda11.8-r15 \
  --cluster vessl-gcp-oregon \
  --preset gpu-l-mem \
  --volume ollama-models:/workspace:500Gi \
  --command "curl -fsSL https://ollama.com/install.sh | sh && \
             ollama serve & sleep 10 && \
             ollama pull qwen3-vl:235b"
```

2. **동일한 볼륨을 재사용**하여 API 서버 Run 생성

### 2. 멀티 GPU 설정

여러 GPU를 사용하려면:

```yaml
resources:
  cluster: vessl-gcp-oregon
  preset: gpu-xl-mem
  gpu_count: 2  # 2개의 GPU 사용

env:
  CUDA_VISIBLE_DEVICES: "0,1"
```

### 3. 로깅 및 모니터링

**로그 확인**:
```bash
# 실시간 로그 스트리밍
vessl run logs <run-number> --follow

# 특정 시간대 로그
vessl run logs <run-number> --since 1h
```

**메트릭 확인**:
- VESSL 웹 UI에서 GPU 사용률, 메모리 등 확인
- Grafana 대시보드 연동 가능

### 4. 환경 변수로 민감 정보 관리

```bash
# Secret 생성
vessl secret create api-keys \
  --from-literal=API_KEY=your_api_key

# Run에서 사용
vessl run create \
  --secret api-keys \
  ...
```

## 🔍 트러블슈팅

### 문제 1: 모델 다운로드 시간 초과

**증상**: 모델 다운로드 중 연결이 끊김

**해결책**:
```bash
# 다운로드 재시도
ollama pull qwen3-vl:235b

# 또는 다운로드 타임아웃 증가
export OLLAMA_DOWNLOAD_TIMEOUT=3600
ollama pull qwen3-vl:235b
```

### 문제 2: GPU 메모리 부족

**증상**: `CUDA out of memory` 오류

**해결책**:
1. 더 큰 GPU 프리셋 사용 (A100 80GB 이상)
2. 더 작은 모델 사용: `qwen3-vl:14b`
3. 양자화 모델 사용: `qwen3-vl:235b-q4`

```bash
# 양자화 모델 다운로드
ollama pull qwen3-vl:235b-q4
```

### 문제 3: 포트 접근 불가

**증상**: API 서버에 접근할 수 없음

**해결책**:
```bash
# 1. Run에서 포트가 제대로 노출되었는지 확인
vessl run read <run-number>

# 2. 로컬에서 포트 포워딩
vessl run port-forward <run-number> 8000:8000

# 3. 방화벽 규칙 확인
# VESSL 웹 UI > Run > Ports 섹션 확인
```

### 문제 4: 디스크 공간 부족

**증상**: "No space left on device" 오류

**해결책**:
```bash
# 1. 불필요한 파일 삭제
rm -rf /tmp/*
docker system prune -a

# 2. 볼륨 크기 증가
# vessl.yaml에서 volume size 증가
mount:
  /workspace:
    volume:
      size: 1000Gi  # 1TB로 증가
```

### 문제 5: Ollama 서버 연결 실패

**증상**: "Ollama 서버에 연결할 수 없습니다"

**해결책**:
```bash
# 1. Ollama 프로세스 확인
ps aux | grep ollama

# 2. Ollama 재시작
pkill ollama
./start_ollama.sh

# 3. 로그 확인
cat ollama.log

# 4. 수동으로 Ollama 시작
ollama serve &
```

## 📊 성능 최적화

### 1. 모델 사전 로드

```python
# server.py에 추가
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 모델 사전 로드"""
    try:
        # 더미 요청으로 모델 로드
        requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": MODEL_NAME, "prompt": "test", "stream": False}
        )
        print("✅ Model preloaded successfully")
    except Exception as e:
        print(f"⚠️  Model preload failed: {e}")
```

### 2. 동시 요청 처리

```bash
# 워커 수 증가
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. 캐싱 활용

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def process_cached_request(prompt_hash):
    # 동일한 요청은 캐시에서 반환
    pass
```

## 📚 추가 자료

- [VESSL 공식 문서](https://docs.vessl.ai/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Qwen3-VL 모델 정보](https://huggingface.co/Qwen)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)

## 💡 유용한 명령어 모음

```bash
# VESSL Run 관리
vessl run list                          # Run 목록
vessl run read <run-number>             # Run 상세 정보
vessl run logs <run-number>             # 로그 확인
vessl run terminate <run-number>        # Run 종료
vessl run port-forward <run-number> 8000:8000  # 포트 포워딩

# Ollama 관리
ollama list                             # 설치된 모델 목록
ollama pull <model-name>                # 모델 다운로드
ollama rm <model-name>                  # 모델 삭제
ollama ps                               # 실행 중인 모델 확인

# 서버 관리
ps aux | grep python                    # Python 프로세스 확인
ps aux | grep ollama                    # Ollama 프로세스 확인
netstat -tulpn | grep 8000              # 포트 사용 확인
curl http://localhost:8000/health       # 헬스체크
```

## ✅ 체크리스트

설치가 완료되면 다음 항목을 확인하세요:

- [ ] Ollama 서버가 실행 중인가? (`ps aux | grep ollama`)
- [ ] 모델이 다운로드되었는가? (`ollama list`)
- [ ] API 서버가 실행 중인가? (`curl http://localhost:8000/`)
- [ ] GPU가 인식되는가? (`nvidia-smi`)
- [ ] 포트가 열려있는가? (`netstat -tulpn | grep 8000`)
- [ ] 헬스체크가 정상인가? (`curl http://localhost:8000/health`)

모든 항목이 체크되었다면 정상적으로 설치가 완료된 것입니다! 🎉

