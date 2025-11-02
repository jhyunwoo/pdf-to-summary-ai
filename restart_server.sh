#!/bin/bash

echo "🔄 서버 재시작 스크립트"
echo "=============================="
echo ""

# Cloudflare Tunnel 재시작 옵션
echo "🌐 Cloudflare Tunnel도 재시작하시겠습니까?"
read -p "Tunnel 재시작? (y/N): " -n 1 -r
echo
echo ""

RESTART_TUNNEL=false
if [[ $REPLY =~ ^[Yy]$ ]]; then
    RESTART_TUNNEL=true
fi

# 기존 서버 프로세스 종료
echo "🛑 기존 서버 프로세스 종료 중..."
pkill -9 -f "python server.py" 2>/dev/null

# Cloudflare Tunnel 종료 (필요 시)
if [ "$RESTART_TUNNEL" = true ]; then
    echo "🛑 Cloudflare Tunnel 종료 중..."
    pkill -f "cloudflared tunnel run" 2>/dev/null
fi

sleep 2

# 프로세스 확인
if pgrep -f "python server.py" > /dev/null; then
    echo "⚠️  일부 프로세스가 여전히 실행 중입니다."
    ps aux | grep "python server.py" | grep -v grep
    exit 1
else
    echo "✅ 모든 서버 프로세스 종료됨"
fi

# 포트 확인
if lsof -i :3000 > /dev/null 2>&1; then
    echo "⚠️  포트 3000이 사용 중입니다."
    lsof -i :3000
    exit 1
fi

# .env 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다!"
    echo "DB_URL을 확인하세요."
fi

echo ""
echo "🚀 서버 시작 중..."
echo ""

# 가상환경 활성화
source venv/bin/activate

# 실행 모드 선택
echo "서버를 어떻게 실행하시겠습니까?"
echo "  1) 포그라운드 (로그가 화면에 표시됨)"
echo "  2) 백그라운드 (로그는 server.log에 저장)"
read -p "선택 (1/2): " -n 1 -r
echo
echo ""

if [[ $REPLY == "2" ]]; then
    # 백그라운드 실행
    nohup python server.py > server.log 2>&1 &
    SERVER_PID=$!
    sleep 2
    
    if ps -p $SERVER_PID > /dev/null; then
        echo "✅ 서버가 백그라운드에서 시작되었습니다! (PID: $SERVER_PID)"
        echo "📊 로그 확인: tail -f server.log"
        
        # Cloudflare Tunnel 시작 (필요 시)
        if [ "$RESTART_TUNNEL" = true ]; then
            echo ""
            echo "🌐 Cloudflare Tunnel 시작 중..."
            ./setup_cloudflare_tunnel.sh start
            
            if [ -f ~/.cloudflared/config.yml ]; then
                DOMAIN=$(grep "hostname:" ~/.cloudflared/config.yml | head -1 | awk '{print $2}')
                if [ ! -z "$DOMAIN" ]; then
                    echo ""
                    echo "✅ 모든 서비스가 재시작되었습니다!"
                    echo ""
                    echo "🌍 외부 접속 주소:"
                    echo "  - https://$DOMAIN"
                    echo "  - https://$DOMAIN/docs"
                    echo "  - https://$DOMAIN/health"
                fi
            fi
        fi
        
        echo ""
        echo "🌐 로컬 접속 주소:"
        echo "  - http://localhost:3000/docs"
        echo "  - http://localhost:3000/health"
    else
        echo "❌ 서버 시작 실패. 로그를 확인하세요: cat server.log"
        exit 1
    fi
else
    # 포그라운드 실행
    if [ "$RESTART_TUNNEL" = true ]; then
        echo "🌐 Cloudflare Tunnel을 백그라운드로 시작합니다..."
        ./setup_cloudflare_tunnel.sh start
        
        if [ -f ~/.cloudflared/config.yml ]; then
            DOMAIN=$(grep "hostname:" ~/.cloudflared/config.yml | head -1 | awk '{print $2}')
            if [ ! -z "$DOMAIN" ]; then
                echo ""
                echo "🌍 외부 접속 주소:"
                echo "  - https://$DOMAIN"
            fi
        fi
        echo ""
    fi
    
    echo "🌐 로컬 접속 주소:"
    echo "  - http://localhost:3000/docs"
    echo "  - http://localhost:3000/health"
    echo ""
    
    python server.py
fi

