#!/bin/bash

# Cloudflare Tunnel 설정 스크립트
# 포트 80, 443을 열 수 없는 환경에서 HTTPS 사용하기

set -e

TUNNEL_NAME="pdf-to-summary-ai"
SERVICE_PORT="3000"  # FastAPI 서버 포트

echo "=== Cloudflare Tunnel 설정 (PDF to Summary AI) ==="
echo ""
echo "이 스크립트는 포트를 열지 않고도 HTTPS를 사용할 수 있게 해줍니다."
echo "내부 포트 $SERVICE_PORT을 Cloudflare Tunnel로 연결합니다."
echo ""

# OS 감지
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    ARCH=$(uname -m)
    if [[ "$ARCH" == "x86_64" ]]; then
        ARCH="amd64"
    elif [[ "$ARCH" == "aarch64" ]]; then
        ARCH="arm64"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="darwin"
    ARCH=$(uname -m)
    if [[ "$ARCH" == "x86_64" ]]; then
        ARCH="amd64"
    elif [[ "$ARCH" == "arm64" ]]; then
        ARCH="arm64"
    fi
else
    echo "지원하지 않는 OS입니다."
    exit 1
fi

# sudo 사용 여부 결정 (root 사용자인 경우 sudo 생략)
if [ "$EUID" -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

# cloudflared 설치 확인
if ! command -v cloudflared &> /dev/null; then
    echo "cloudflared를 설치합니다..."
    
    if [[ "$OS" == "linux" ]]; then
        # Linux 설치
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-${OS}-${ARCH} -O cloudflared
        $SUDO mv cloudflared /usr/local/bin/
        $SUDO chmod +x /usr/local/bin/cloudflared
    elif [[ "$OS" == "darwin" ]]; then
        # macOS 설치
        if command -v brew &> /dev/null; then
            brew install cloudflared
        else
            curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-${OS}-${ARCH}.tgz -o cloudflared.tgz
            tar -xzf cloudflared.tgz
            $SUDO mv cloudflared /usr/local/bin/
            $SUDO chmod +x /usr/local/bin/cloudflared
            rm cloudflared.tgz
        fi
    fi
    
    echo "✓ cloudflared 설치 완료"
else
    echo "✓ cloudflared가 이미 설치되어 있습니다"
fi

echo ""
echo "=== 다음 단계를 따라주세요 ==="
echo ""
echo "1. Cloudflare 로그인 (브라우저가 열립니다):"
echo "   cloudflared tunnel login"
echo ""
echo "2. Tunnel 생성:"
echo "   cloudflared tunnel create $TUNNEL_NAME"
echo ""
echo "3. Tunnel ID 확인 (위 명령어 출력에서 복사):"
echo "   [출력 예시: Created tunnel $TUNNEL_NAME with id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]"
echo ""
echo "4. 설정 파일 생성:"
echo "   이 스크립트를 다시 실행하거나 수동으로 설정하세요."
echo "   ./setup_cloudflare_tunnel.sh configure <TUNNEL_ID> <DOMAIN>"
echo ""
echo "=== 자동 설정을 원하시면 ==="
echo "1. 먼저 수동으로 위 1-2번 단계를 실행하세요"
echo "2. 그 다음 이 명령어를 실행하세요:"
echo "   ./setup_cloudflare_tunnel.sh configure <TUNNEL_ID> api.your-domain.com"
echo ""
echo "예시:"
echo "   ./setup_cloudflare_tunnel.sh configure abc123-456-def api.moveto.kr"
echo ""

# configure 모드
if [ "$1" = "configure" ]; then
    TUNNEL_ID=$2
    DOMAIN=$3
    
    if [ -z "$TUNNEL_ID" ] || [ -z "$DOMAIN" ]; then
        echo "❌ 오류: TUNNEL_ID와 DOMAIN이 필요합니다"
        echo ""
        echo "사용법: $0 configure <TUNNEL_ID> <DOMAIN>"
        echo ""
        echo "예시:"
        echo "  $0 configure abc123-456-def api.moveto.kr"
        exit 1
    fi
    
    echo "=== Tunnel 설정 중 ==="
    echo "  Tunnel ID: $TUNNEL_ID"
    echo "  Domain: $DOMAIN"
    echo "  Service: http://localhost:$SERVICE_PORT"
    echo ""
    
    # 설정 디렉토리 생성
    mkdir -p ~/.cloudflared
    
    # 설정 파일 생성
    cat > ~/.cloudflared/config.yml <<EOF
tunnel: $TUNNEL_ID
credentials-file: $HOME/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: $DOMAIN
    service: http://localhost:$SERVICE_PORT
  - service: http_status:404
EOF
    
    echo "✓ 설정 파일 생성 완료: ~/.cloudflared/config.yml"
    
    # DNS 라우팅 설정
    echo ""
    echo "DNS 라우팅을 설정합니다..."
    cloudflared tunnel route dns $TUNNEL_NAME $DOMAIN
    
    echo ""
    echo "=== 설정 완료! ==="
    echo ""
    echo "📝 설정 내용:"
    echo "  - Tunnel 이름: $TUNNEL_NAME"
    echo "  - Tunnel ID: $TUNNEL_ID"
    echo "  - 도메인: $DOMAIN"
    echo "  - 내부 포트: $SERVICE_PORT"
    echo ""
    echo "🚀 Tunnel을 시작하려면:"
    echo "  cloudflared tunnel run $TUNNEL_NAME"
    echo ""
    echo "🔧 백그라운드로 실행하려면:"
    echo "  nohup cloudflared tunnel run $TUNNEL_NAME > cloudflared.log 2>&1 &"
    echo ""
    echo "⚙️  systemd 서비스로 등록하려면 (Linux):"
    if [ "$EUID" -eq 0 ]; then
        echo "  cloudflared service install"
        echo "  systemctl start cloudflared"
        echo "  systemctl enable cloudflared"
    else
        echo "  sudo cloudflared service install"
        echo "  sudo systemctl start cloudflared"
        echo "  sudo systemctl enable cloudflared"
    fi
    echo ""
    echo "✅ 이제 https://$DOMAIN 으로 접속할 수 있습니다!"
    echo ""
    echo "⚠️  주의: API 서버(포트 $SERVICE_PORT)가 실행 중인지 확인하세요:"
    echo "  ./run_server.sh"
    echo ""
fi

# status 모드
if [ "$1" = "status" ]; then
    echo "=== Cloudflare Tunnel 상태 확인 ==="
    echo ""
    
    if ! command -v cloudflared &> /dev/null; then
        echo "❌ cloudflared가 설치되어 있지 않습니다"
        exit 1
    fi
    
    echo "📋 Tunnel 목록:"
    cloudflared tunnel list
    echo ""
    
    if [ -f ~/.cloudflared/config.yml ]; then
        echo "✓ 설정 파일 존재: ~/.cloudflared/config.yml"
        echo ""
        echo "설정 내용:"
        cat ~/.cloudflared/config.yml
    else
        echo "❌ 설정 파일이 없습니다: ~/.cloudflared/config.yml"
    fi
    echo ""
fi

# start 모드 - 백그라운드로 실행
if [ "$1" = "start" ]; then
    echo "=== Cloudflare Tunnel 시작 ==="
    
    if [ ! -f ~/.cloudflared/config.yml ]; then
        echo "❌ 설정 파일이 없습니다. 먼저 configure를 실행하세요."
        exit 1
    fi
    
    # 이미 실행 중인지 확인
    if pgrep -f "cloudflared tunnel run" > /dev/null; then
        echo "⚠️  Cloudflare Tunnel이 이미 실행 중입니다"
        echo ""
        echo "중지하려면: ./setup_cloudflare_tunnel.sh stop"
        exit 0
    fi
    
    echo "🚀 Tunnel을 백그라운드로 시작합니다..."
    nohup cloudflared tunnel run $TUNNEL_NAME > cloudflared.log 2>&1 &
    
    sleep 2
    
    if pgrep -f "cloudflared tunnel run" > /dev/null; then
        echo "✅ Tunnel이 성공적으로 시작되었습니다"
        echo ""
        echo "로그 확인: tail -f cloudflared.log"
    else
        echo "❌ Tunnel 시작 실패. 로그를 확인하세요:"
        echo "  cat cloudflared.log"
    fi
fi

# stop 모드
if [ "$1" = "stop" ]; then
    echo "=== Cloudflare Tunnel 중지 ==="
    
    if pgrep -f "cloudflared tunnel run" > /dev/null; then
        echo "🛑 Tunnel을 중지합니다..."
        pkill -f "cloudflared tunnel run"
        sleep 1
        echo "✅ Tunnel이 중지되었습니다"
    else
        echo "⚠️  실행 중인 Tunnel이 없습니다"
    fi
fi

# help 또는 인자 없음
if [ -z "$1" ] || [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    if [ "$1" != "help" ] && [ "$1" != "--help" ] && [ "$1" != "-h" ]; then
        # 설치 안내는 이미 위에서 표시됨
        echo ""
    fi
    
    echo "=== 사용법 ==="
    echo ""
    echo "  $0 configure <TUNNEL_ID> <DOMAIN>  - Tunnel 설정"
    echo "  $0 start                            - Tunnel 시작 (백그라운드)"
    echo "  $0 stop                             - Tunnel 중지"
    echo "  $0 status                           - Tunnel 상태 확인"
    echo "  $0 help                             - 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0 configure abc123-456-def api.moveto.kr"
    echo "  $0 start"
    echo "  $0 stop"
    echo ""
fi

