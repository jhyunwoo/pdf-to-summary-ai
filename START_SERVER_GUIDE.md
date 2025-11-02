# 서버 시작 가이드

## 🚀 빠른 시작

### 방법 1: 자동 스크립트 사용 (권장)

```bash
./run_server.sh
```

이 스크립트는 다음을 자동으로 처리합니다:
- ✅ 가상환경 활성화
- ✅ Ollama 서버 상태 확인 및 시작
- ✅ Gemma3 모델 확인
- ✅ **Cloudflare Tunnel 시작 옵션**
- ✅ API 서버 시작 (포그라운드/백그라운드 선택)

### 방법 2: 수동 시작

```bash
# 가상환경 활성화
source venv/bin/activate

# Ollama 서버 시작 (별도 터미널)
./start_ollama.sh

# API 서버 시작
python server.py
```

## 🌐 Cloudflare Tunnel 통합

### Tunnel 설정 (최초 1회)

```bash
# 1. Cloudflare 로그인
cloudflared tunnel login

# 2. Tunnel 생성
cloudflared tunnel create pdf-to-summary-ai

# 3. 설정 (Tunnel ID와 도메인 입력)
./setup_cloudflare_tunnel.sh configure <TUNNEL_ID> <도메인>
```

예시:
```bash
./setup_cloudflare_tunnel.sh configure abc123-456-def api.moveto.kr
```

### 서버와 Tunnel 함께 시작

```bash
./run_server.sh
```

실행 시:
1. "Cloudflare Tunnel을 시작하시겠습니까?" → **Y** 입력
2. "서버를 어떻게 실행하시겠습니까?" → **2** (백그라운드) 권장

출력 예시:
```
✅ 서버가 백그라운드에서 시작되었습니다! (PID: 12345)
✅ 모든 서비스가 시작되었습니다!

📋 실행 중인 서비스:
  - API 서버 (PID: 12345)
  - Cloudflare Tunnel

🌍 외부 접속 주소:
  - https://api.moveto.kr
  - https://api.moveto.kr/docs
  - https://api.moveto.kr/health
```

## 🔄 서버 재시작

### 자동 재시작

```bash
./restart_server.sh
```

옵션:
- Cloudflare Tunnel 재시작 여부 선택 가능
- 포그라운드/백그라운드 실행 모드 선택

### 수동 재시작

```bash
# 서버 중지
pkill -f "python server.py"

# Tunnel 중지 (필요 시)
pkill -f "cloudflared tunnel run"

# 다시 시작
./run_server.sh
```

## 🛑 서버 중지

### 모든 서비스 중지

```bash
./stop_all.sh
```

다음을 모두 중지합니다:
- API 서버
- Ollama 서버
- Cloudflare Tunnel

### 개별 중지

```bash
# API 서버만 중지
pkill -f "python server.py"

# Cloudflare Tunnel만 중지
./setup_cloudflare_tunnel.sh stop

# Ollama 서버 중지
pkill ollama
```

## 📊 서버 상태 확인

### API 서버

```bash
# 프로세스 확인
ps aux | grep "python server.py"

# 헬스체크
curl http://localhost:3000/health

# 로그 확인
tail -f server.log
```

### Cloudflare Tunnel

```bash
# 상태 확인
./setup_cloudflare_tunnel.sh status

# 프로세스 확인
ps aux | grep "cloudflared tunnel"

# 로그 확인
tail -f cloudflared.log
```

## 🔧 실행 모드 비교

### 포그라운드 모드

**장점:**
- 실시간 로그 확인 가능
- 디버깅에 유리
- Ctrl+C로 즉시 종료

**단점:**
- 터미널 종료 시 서버도 종료
- 터미널이 계속 점유됨

**사용 시기:**
- 개발/테스트
- 디버깅
- 임시 실행

### 백그라운드 모드

**장점:**
- 터미널 독립적으로 실행
- 서버 재부팅까지 계속 실행
- 로그 파일로 기록

**단점:**
- 실시간 로그를 직접 볼 수 없음
- 프로세스 관리 필요

**사용 시기:**
- 프로덕션 환경
- 장기 실행
- 안정적인 서비스 제공

## 📝 환경 변수

서버 시작 전 환경 변수를 설정할 수 있습니다:

```bash
# .env 파일 생성
cat > .env <<EOF
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=gemma3:27b
PORT=3000
HOST=0.0.0.0
DB_URL=postgresql://user:password@localhost/dbname
EOF
```

또는 직접 export:

```bash
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=gemma3:27b
export PORT=3000
export HOST=0.0.0.0
```

## 🌍 접속 URL

### 로컬 접속

- **API 문서**: http://localhost:3000/docs
- **헬스체크**: http://localhost:3000/health
- **루트**: http://localhost:3000/

### 외부 접속 (Cloudflare Tunnel 사용 시)

- **API 문서**: https://your-domain.com/docs
- **헬스체크**: https://your-domain.com/health
- **API 엔드포인트**: https://your-domain.com/api/generate

## 🔍 문제 해결

### 서버가 시작되지 않음

```bash
# 포트 확인
lsof -i :3000

# 프로세스 확인
ps aux | grep "python server.py"

# 로그 확인
cat server.log

# 강제 종료 후 재시작
pkill -9 -f "python server.py"
./run_server.sh
```

### Ollama 연결 실패

```bash
# Ollama 상태 확인
curl http://localhost:11434/api/tags

# Ollama 재시작
./start_ollama.sh
```

### Cloudflare Tunnel 연결 실패

```bash
# 설정 확인
./setup_cloudflare_tunnel.sh status

# 재시작
./setup_cloudflare_tunnel.sh stop
./setup_cloudflare_tunnel.sh start

# 로그 확인
cat cloudflared.log
```

### 데이터베이스 연결 실패

```bash
# .env 파일 확인
cat .env

# DB_URL 형식 확인
# postgresql://user:password@host:port/database

# PostgreSQL 연결 테스트
psql -h host -U user -d database
```

## 📚 관련 문서

- **Cloudflare Tunnel 상세 가이드**: `CLOUDFLARE_TUNNEL_GUIDE.md`
- **데이터베이스 설정**: `DB_SETUP_GUIDE.md`
- **API 사용법**: `API_USAGE_GUIDE.md`
- **전체 설정 가이드**: `SETUP_SUMMARY.md`

## 💡 팁

### systemd 서비스 등록 (Linux)

프로덕션 환경에서는 systemd 서비스로 등록하는 것을 권장합니다:

```bash
# API 서버 서비스
sudo cat > /etc/systemd/system/pdf-to-summary-api.service <<EOF
[Unit]
Description=PDF to Summary AI API Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/pdf-to-summary-ai
ExecStart=/path/to/pdf-to-summary-ai/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl start pdf-to-summary-api
sudo systemctl enable pdf-to-summary-api
```

### Cloudflare Tunnel systemd 서비스

```bash
# Tunnel을 시스템 서비스로 등록
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

---

**모든 서비스를 한 번에 시작**: `./run_server.sh` → Y (Tunnel) → 2 (백그라운드)  
**모든 서비스 중지**: `./stop_all.sh`

