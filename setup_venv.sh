#!/bin/bash
# Python 가상환경 설정 스크립트

set -e

echo "🐍 Python 가상환경 설정을 시작합니다..."
echo ""

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되어 있지 않습니다."
    echo "   Python 3.9 이상을 설치해주세요."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python 버전: $PYTHON_VERSION"
echo ""

# 최소 버전 확인 (3.9 이상)
REQUIRED_VERSION="3.9"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "❌ Python 3.9 이상이 필요합니다."
    echo "   현재 버전: $PYTHON_VERSION"
    exit 1
fi

# 가상환경 디렉토리 이름
VENV_DIR="venv"

# 기존 가상환경이 있으면 물어보기
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  기존 가상환경이 발견되었습니다: $VENV_DIR"
    read -p "삭제하고 새로 만드시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  기존 가상환경 삭제 중..."
        rm -rf "$VENV_DIR"
    else
        echo "✅ 기존 가상환경을 사용합니다."
        source "$VENV_DIR/bin/activate"
        python --version
        exit 0
    fi
fi

# 가상환경 생성
echo "📦 가상환경 생성 중: $VENV_DIR"
python3 -m venv "$VENV_DIR"

if [ $? -eq 0 ]; then
    echo "✅ 가상환경 생성 완료"
else
    echo "❌ 가상환경 생성 실패"
    exit 1
fi

echo ""

# 가상환경 활성화
echo "🔄 가상환경 활성화 중..."
source "$VENV_DIR/bin/activate"

# pip 업그레이드
echo "📦 pip 업그레이드 중..."
pip install --upgrade pip setuptools wheel

echo ""

# 의존성 설치
if [ -f "requirements.txt" ]; then
    echo "📦 Python 패키지 설치 중..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ 패키지 설치 완료"
    else
        echo "❌ 패키지 설치 실패"
        exit 1
    fi
else
    echo "⚠️  requirements.txt 파일을 찾을 수 없습니다."
fi

echo ""
echo "🎉 Python 가상환경 설정이 완료되었습니다!"
echo ""
echo "가상환경 활성화 방법:"
echo "  source venv/bin/activate"
echo ""
echo "가상환경 비활성화 방법:"
echo "  deactivate"
echo ""
echo "설치된 패키지 확인:"
pip list
echo ""

