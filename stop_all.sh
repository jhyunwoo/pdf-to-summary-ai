#!/bin/bash
# 모든 서비스 종료 스크립트

echo "🛑 서비스 종료 중..."
echo ""

# API 서버 종료
echo "📍 API 서버 종료 중..."
if pgrep -f "python server.py" > /dev/null; then
    pkill -f "python server.py"
    echo "✅ API 서버가 종료되었습니다."
else
    echo "ℹ️  실행 중인 API 서버가 없습니다."
fi

echo ""

# Ollama 서버 종료
echo "📍 Ollama 서버 종료 중..."
if pgrep -x "ollama" > /dev/null; then
    pkill ollama
    sleep 2
    if pgrep -x "ollama" > /dev/null; then
        # 강제 종료
        pkill -9 ollama
    fi
    echo "✅ Ollama 서버가 종료되었습니다."
else
    echo "ℹ️  실행 중인 Ollama 서버가 없습니다."
fi

echo ""

# 프로세스 확인
echo "🔍 실행 중인 프로세스 확인..."
if pgrep -x "ollama" > /dev/null || pgrep -f "python server.py" > /dev/null; then
    echo "⚠️  일부 프로세스가 아직 실행 중입니다:"
    ps aux | grep -E "ollama|python server.py" | grep -v grep
else
    echo "✅ 모든 서비스가 종료되었습니다."
fi

echo ""

