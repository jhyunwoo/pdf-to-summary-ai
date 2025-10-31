#!/bin/bash
# Ollama 설치 스크립트 (VESSL 환경용)

set -e  # 오류 발생 시 스크립트 중단

echo "🚀 Ollama 설치를 시작합니다..."

# 1. 시스템 정보 확인
echo "📋 시스템 정보:"
uname -a
echo ""

# 2. GPU 확인 (NVIDIA GPU가 있는 경우)
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 GPU 정보:"
    nvidia-smi
    echo ""
else
    echo "⚠️  NVIDIA GPU를 찾을 수 없습니다. CPU 모드로 실행됩니다."
    echo ""
fi

# 3. Ollama 다운로드 및 설치
echo "📥 Ollama 다운로드 중..."

if [ -f "/usr/local/bin/ollama" ]; then
    echo "✅ Ollama가 이미 설치되어 있습니다."
    /usr/local/bin/ollama --version
else
    # Ollama 설치
    curl -fsSL https://ollama.com/install.sh | sh
    
    if [ $? -eq 0 ]; then
        echo "✅ Ollama 설치 완료"
        ollama --version
    else
        echo "❌ Ollama 설치 실패"
        exit 1
    fi
fi

echo ""
echo "🎉 Ollama 설치가 완료되었습니다!"
echo ""
echo "다음 단계:"
echo "1. Ollama 서버 시작: ./start_ollama.sh"
echo "2. 모델 다운로드: ./download_model.sh"
echo "3. Python 서버 시작: python server.py"

