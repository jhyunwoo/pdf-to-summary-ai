#!/bin/bash
# Qwen3-VL:235b 모델 다운로드 스크립트

set -e

MODEL_NAME="qwen3-vl:235b"

echo "📥 모델 다운로드를 시작합니다: $MODEL_NAME"
echo ""
echo "⚠️  주의: 이 모델은 매우 크므로 (약 235GB) 다운로드에 오랜 시간이 걸립니다."
echo "         충분한 디스크 공간이 있는지 확인하세요."
echo ""

# 디스크 공간 확인
echo "💾 현재 디스크 사용량:"
df -h /workspace 2>/dev/null || df -h .
echo ""

read -p "계속하시겠습니까? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "다운로드를 취소했습니다."
    exit 0
fi

# Ollama 서버가 실행 중인지 확인
if ! pgrep -x "ollama" > /dev/null; then
    echo "❌ Ollama 서버가 실행되지 않았습니다."
    echo "먼저 './start_ollama.sh' 를 실행하세요."
    exit 1
fi

# 모델 다운로드
echo "📦 모델 다운로드 중..."
echo "이 작업은 수 시간이 걸릴 수 있습니다..."
echo ""

ollama pull $MODEL_NAME

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 모델 다운로드 완료: $MODEL_NAME"
    echo ""
    echo "📋 설치된 모델 목록:"
    ollama list
    echo ""
    echo "🧪 모델 테스트:"
    echo "   ollama run $MODEL_NAME"
else
    echo ""
    echo "❌ 모델 다운로드 실패"
    exit 1
fi

