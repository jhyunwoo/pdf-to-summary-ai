#!/bin/bash
# API 서버 실행 스크립트

set -e

echo "🌐 Ollama Qwen3-VL API 서버 시작"
echo "================================"
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. 가상환경 확인 및 활성화
if [ -d "venv" ]; then
    echo "✅ 가상환경 발견"
    source venv/bin/activate
    echo "✅ 가상환경 활성화됨"
else
    echo -e "${YELLOW}⚠️  가상환경이 없습니다.${NC}"
    echo "먼저 './setup_venv.sh' 또는 './quick_start.sh'를 실행하세요."
    exit 1
fi

echo ""

# 2. Ollama 서버 상태 확인
echo "🔍 Ollama 서버 상태 확인 중..."
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama 서버가 실행 중입니다."
else
    echo -e "${YELLOW}⚠️  Ollama 서버가 실행되지 않았습니다.${NC}"
    echo "Ollama 서버를 시작하시겠습니까? (y/n)"
    read -p "입력: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        chmod +x start_ollama.sh
        ./start_ollama.sh
        sleep 5
    else
        echo -e "${RED}❌ Ollama 서버가 필요합니다.${NC}"
        echo "나중에 './start_ollama.sh'를 실행하여 Ollama를 시작하세요."
        exit 1
    fi
fi

echo ""

# 3. 모델 확인
echo "🤖 모델 확인 중..."
if ollama list | grep -q "qwen3-vl"; then
    echo "✅ Qwen3-VL 모델이 설치되어 있습니다."
else
    echo -e "${YELLOW}⚠️  Qwen3-VL 모델이 설치되어 있지 않습니다.${NC}"
    echo "나중에 './download_model.sh'를 실행하여 모델을 다운로드하세요."
fi

echo ""

# 4. 환경 변수 설정
export OLLAMA_HOST=${OLLAMA_HOST:-"http://localhost:11434"}
export MODEL_NAME=${MODEL_NAME:-"qwen3-vl:32b"}
export PORT=${PORT:-3000}
export HOST=${HOST:-"0.0.0.0"}

echo "📋 서버 설정:"
echo "  - Ollama Host: $OLLAMA_HOST"
echo "  - Model: $MODEL_NAME"
echo "  - API Host: $HOST:$PORT"
echo ""

# 5. 서버 시작
echo "🚀 API 서버를 시작합니다..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 백그라운드로 실행할지 물어보기
echo "서버를 어떻게 실행하시겠습니까?"
echo "  1) 포그라운드 (로그가 화면에 표시됨, Ctrl+C로 종료)"
echo "  2) 백그라운드 (백그라운드에서 실행, 로그는 server.log에 저장)"
read -p "선택 (1/2): " -n 1 -r
echo
echo ""

if [[ $REPLY == "2" ]]; then
    # 백그라운드 실행
    echo "📝 백그라운드로 실행 중..."
    nohup python server.py > server.log 2>&1 &
    SERVER_PID=$!
    
    sleep 3
    
    if ps -p $SERVER_PID > /dev/null; then
        echo "✅ 서버가 백그라운드에서 시작되었습니다! (PID: $SERVER_PID)"
        echo ""
        echo "📊 로그 확인: tail -f server.log"
        echo "🛑 서버 종료: kill $SERVER_PID"
        echo "   또는: pkill -f 'python server.py'"
        echo ""
        echo "🌐 서버 주소:"
        echo "  - API 문서: http://localhost:$PORT/docs"
        echo "  - 서버 상태: http://localhost:$PORT/health"
    else
        echo -e "${RED}❌ 서버 시작에 실패했습니다.${NC}"
        echo "로그를 확인하세요: cat server.log"
        exit 1
    fi
else
    # 포그라운드 실행
    echo "🌐 서버 주소:"
    echo "  - API 문서: http://localhost:$PORT/docs"
    echo "  - 서버 상태: http://localhost:$PORT/health"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    python server.py
fi

