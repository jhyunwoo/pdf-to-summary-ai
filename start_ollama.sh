#!/bin/bash
# Ollama 서버 시작 스크립트

set -e

echo "🚀 Ollama 서버를 시작합니다..."

# Ollama 서버가 이미 실행 중인지 확인
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama 서버가 이미 실행 중입니다."
    exit 0
fi

# 환경 변수 설정
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=/workspace/.ollama/models  # VESSL에서 모델 저장 경로

# 모델 디렉토리 생성
mkdir -p /workspace/.ollama/models

echo "📍 Ollama 서버 설정:"
echo "   - Host: $OLLAMA_HOST"
echo "   - Models Path: $OLLAMA_MODELS"
echo ""

# Ollama 서버 백그라운드로 시작
nohup ollama serve > ollama.log 2>&1 &

# 서버 시작 대기
echo "⏳ 서버 시작 대기 중..."
sleep 5

# 서버 상태 확인
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama 서버가 성공적으로 시작되었습니다!"
    echo "📊 로그 확인: tail -f ollama.log"
else
    echo "❌ Ollama 서버 시작 실패"
    echo "로그를 확인하세요: cat ollama.log"
    exit 1
fi

