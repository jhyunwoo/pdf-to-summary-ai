# Cloudflare Tunnel 설정 가이드

Cloudflare Tunnel을 사용하면 포트 80, 443을 열지 않고도 내부 서버를 HTTPS로 공개할 수 있습니다.

## 🎯 장점

- ✅ **포트 개방 불필요**: 방화벽 설정 없이 서비스 제공
- ✅ **자동 HTTPS**: SSL/TLS 인증서 자동 관리
- ✅ **DDoS 보호**: Cloudflare의 보안 기능 활용
- ✅ **무료**: Cloudflare 계정만 있으면 사용 가능
- ✅ **간편한 설정**: 명령어 몇 개로 설정 완료

## 📋 사전 준비

1. **Cloudflare 계정** (무료)
   - https://dash.cloudflare.com 에서 가입

2. **도메인** (Cloudflare에 등록된 도메인)
   - 기존 도메인을 Cloudflare로 이전하거나
   - Cloudflare에서 새 도메인 구매

3. **서버 실행 중**
   - FastAPI 서버가 포트 3000에서 실행 중이어야 함

## 🚀 빠른 시작

### 1단계: 스크립트 실행

```bash
./setup_cloudflare_tunnel.sh
```

cloudflared가 자동으로 설치됩니다.

### 2단계: Cloudflare 로그인

```bash
cloudflared tunnel login
```

브라우저가 열리면 Cloudflare에 로그인하고 권한을 승인하세요.

### 3단계: Tunnel 생성

```bash
cloudflared tunnel create pdf-to-summary-ai
```

출력 예시:
```
Tunnel credentials written to /Users/yourname/.cloudflared/abc123-456-def.json
Created tunnel pdf-to-summary-ai with id abc123-456-def
```

**⚠️ 중요**: `abc123-456-def` 같은 Tunnel ID를 복사하세요!

### 4단계: 설정

```bash
./setup_cloudflare_tunnel.sh configure <TUNNEL_ID> <도메인>
```

예시:
```bash
./setup_cloudflare_tunnel.sh configure abc123-456-def api.moveto.kr
```

### 5단계: Tunnel 시작

```bash
./setup_cloudflare_tunnel.sh start
```

또는 직접 실행:
```bash
cloudflared tunnel run pdf-to-summary-ai
```

## 📖 스크립트 사용법

### 전체 명령어

```bash
# 설정
./setup_cloudflare_tunnel.sh configure <TUNNEL_ID> <DOMAIN>

# 시작 (백그라운드)
./setup_cloudflare_tunnel.sh start

# 중지
./setup_cloudflare_tunnel.sh stop

# 상태 확인
./setup_cloudflare_tunnel.sh status

# 도움말
./setup_cloudflare_tunnel.sh help
```

### 예제 시나리오

#### 시나리오 1: 처음 설정하기

```bash
# 1. 스크립트 실행 (cloudflared 설치)
./setup_cloudflare_tunnel.sh

# 2. 로그인
cloudflared tunnel login

# 3. Tunnel 생성
cloudflared tunnel create pdf-to-summary-ai
# 출력에서 Tunnel ID 복사: abc123-456-def

# 4. 설정
./setup_cloudflare_tunnel.sh configure abc123-456-def api.moveto.kr

# 5. 시작
./setup_cloudflare_tunnel.sh start

# 6. 확인
curl https://api.moveto.kr/health
```

#### 시나리오 2: 서버 재시작 후

```bash
# API 서버 시작
./run_server.sh

# Tunnel 시작
./setup_cloudflare_tunnel.sh start
```

#### 시나리오 3: 문제 해결

```bash
# 상태 확인
./setup_cloudflare_tunnel.sh status

# Tunnel 중지
./setup_cloudflare_tunnel.sh stop

# 로그 확인
tail -f cloudflared.log

# 다시 시작
./setup_cloudflare_tunnel.sh start
```

## 🔧 고급 설정

### systemd 서비스로 등록 (Linux)

서버 재부팅 시 자동으로 Tunnel이 시작되도록 설정:

```bash
# 서비스 설치
sudo cloudflared service install

# 서비스 시작
sudo systemctl start cloudflared

# 자동 시작 활성화
sudo systemctl enable cloudflared

# 상태 확인
sudo systemctl status cloudflared
```

### 여러 서비스 연결

`~/.cloudflared/config.yml` 파일을 수정:

```yaml
tunnel: abc123-456-def
credentials-file: /home/user/.cloudflared/abc123-456-def.json

ingress:
  # API 서버
  - hostname: api.moveto.kr
    service: http://localhost:3000
  
  # 프론트엔드 (예시)
  - hostname: app.moveto.kr
    service: http://localhost:8080
  
  # 기본 404
  - service: http_status:404
```

### 로그 레벨 조정

```bash
# 디버그 모드로 실행
cloudflared tunnel --loglevel debug run pdf-to-summary-ai
```

## 🔍 문제 해결

### 문제 1: "tunnel not found"

**원인**: Tunnel이 생성되지 않았거나 잘못된 이름 사용

**해결**:
```bash
# Tunnel 목록 확인
cloudflared tunnel list

# 새로 생성
cloudflared tunnel create pdf-to-summary-ai
```

### 문제 2: "connection refused"

**원인**: API 서버가 실행 중이지 않음

**해결**:
```bash
# 서버 실행 확인
curl http://localhost:3000/health

# 서버 시작
./run_server.sh
```

### 문제 3: "DNS 레코드가 업데이트되지 않음"

**원인**: DNS 전파 지연

**해결**:
```bash
# DNS 강제 설정
cloudflared tunnel route dns pdf-to-summary-ai api.moveto.kr

# 확인 (몇 분 소요 가능)
nslookup api.moveto.kr
```

### 문제 4: 백그라운드 실행 후 멈춤

**원인**: 로그 파일이 너무 커짐

**해결**:
```bash
# 로그 파일 정리
rm cloudflared.log

# 로그 로테이션 설정으로 재시작
nohup cloudflared tunnel run pdf-to-summary-ai > cloudflared.log 2>&1 &
```

## 📊 모니터링

### 로그 확인

```bash
# 실시간 로그
tail -f cloudflared.log

# 최근 100줄
tail -n 100 cloudflared.log

# 에러만 필터링
grep ERROR cloudflared.log
```

### 연결 상태 확인

```bash
# Tunnel 상태
cloudflared tunnel info pdf-to-summary-ai

# 실행 중인 프로세스
ps aux | grep cloudflared
```

### Cloudflare Dashboard

https://dash.cloudflare.com 에서:
1. Zero Trust > Access > Tunnels 메뉴
2. Tunnel 상태 및 트래픽 확인 가능

## 🔐 보안 권장사항

1. **Tunnel Credentials 보호**
   ```bash
   # credentials 파일 권한 설정
   chmod 600 ~/.cloudflared/*.json
   ```

2. **API 접근 제한** (선택)
   - Cloudflare Access를 사용하여 IP 기반 제한
   - API 키 인증 추가

3. **로그 관리**
   ```bash
   # 민감한 정보가 로그에 기록되지 않도록 주의
   # 정기적으로 로그 정리
   ```

## 💰 비용

- **Cloudflare Tunnel**: 무료
- **트래픽**: 무료 (무제한)
- **도메인**: 별도 (Cloudflare에서 구매 시 약 $10/년)

## 🆚 다른 방법과 비교

| 방법 | 장점 | 단점 |
|------|------|------|
| **Cloudflare Tunnel** | 무료, 간편, 보안 | Cloudflare 의존 |
| **ngrok** | 간편 | 유료 (커스텀 도메인), 느림 |
| **직접 포트 개방** | 제어 가능 | 복잡, 보안 위험 |
| **리버스 프록시** | 유연함 | 설정 복잡, 유지보수 필요 |

## 📚 추가 자료

- [Cloudflare Tunnel 공식 문서](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [cloudflared CLI 참조](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/)

## ❓ FAQ

**Q: 여러 도메인을 연결할 수 있나요?**
A: 네, config.yml에서 여러 hostname을 설정하면 됩니다.

**Q: 서버 재시작 시 자동으로 실행되나요?**
A: systemd 서비스로 등록하면 자동으로 실행됩니다.

**Q: 다른 포트로 변경하려면?**
A: config.yml에서 `service: http://localhost:포트번호` 부분을 수정하세요.

**Q: HTTPS만 되나요? WebSocket도 지원하나요?**
A: 네, HTTP, HTTPS, WebSocket 모두 지원합니다.

**Q: 무료 플랜 제한이 있나요?**
A: Tunnel 자체는 무료이며, 트래픽 제한도 없습니다.

---

**문의사항이 있으면 이슈를 생성하거나 Cloudflare 커뮤니티에 문의하세요.**

