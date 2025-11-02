#!/bin/bash
# 빠른 시작 스크립트

echo "🚀 Ollama Gemma3 서버 빠른 시작 가이드"
echo "================================================"
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 함수: 단계 출력
print_step() {
    echo -e "${GREEN}[단계 $1]${NC} $2"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1단계: 필요한 파일 확인
print_step "1" "필요한 파일 확인 중..."
required_files=("server.py" "requirements.txt" "setup_ollama.sh" "start_ollama.sh" "download_model.sh" "setup_venv.sh")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "필수 파일이 없습니다: $file"
        exit 1
    fi
done
echo "✅ 모든 필요한 파일이 있습니다."
echo ""

# 2단계: Python 확인
print_step "2" "Python 설치 확인 중..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3가 설치되어 있지 않습니다."
    exit 1
fi
python_version=$(python3 --version)
echo "✅ $python_version"
echo ""

# 3단계: Python 가상환경 설정
print_step "3" "Python 가상환경 설정 중..."
chmod +x setup_venv.sh
./setup_venv.sh

# 가상환경 활성화 확인
if [ -d "venv" ]; then
    echo "✅ 가상환경이 생성되었습니다."
    source venv/bin/activate
    echo "✅ 가상환경이 활성화되었습니다."
else
    print_error "가상환경 생성에 실패했습니다."
    exit 1
fi
echo ""

# 4단계: 실행 권한 부여
print_step "4" "스크립트 실행 권한 부여 중..."
chmod +x setup_ollama.sh start_ollama.sh download_model.sh
echo "✅ 실행 권한 부여 완료"
echo ""

# 5단계: Ollama 설치
print_step "5" "Ollama 설치 확인 중..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama가 이미 설치되어 있습니다."
else
    print_warning "Ollama를 설치합니다..."
    ./setup_ollama.sh
fi
echo ""

# 6단계: Ollama 서버 시작
print_step "6" "Ollama 서버 시작 중..."
./start_ollama.sh
echo ""

# 7단계: 모델 확인
print_step "7" "Gemma3:27b 모델 확인 중..."
if ollama list | grep -q "gemma3:27b"; then
    echo "✅ 모델이 이미 설치되어 있습니다."
else
    print_warning "모델이 설치되어 있지 않습니다."
    echo ""
    echo "모델을 다운로드하시겠습니까? (y/n)"
    echo "⚠️  주의: 모델 크기가 약 27GB이며 다운로드에 시간이 걸립니다."
    read -p "입력: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./download_model.sh
    else
        print_warning "나중에 './download_model.sh'를 실행하여 모델을 다운로드하세요."
    fi
fi
echo ""

# 8단계: API 서버 시작
print_step "8" "API 서버 시작 준비 완료"
echo ""
echo "================================================"
echo "✨ 설정이 완료되었습니다!"
echo "================================================"
echo ""
echo "다음 명령어로 API 서버를 시작하세요:"
echo "  ${GREEN}python server.py${NC}"
echo ""
echo "또는 백그라운드로 실행:"
echo "  ${GREEN}nohup python server.py > server.log 2>&1 &${NC}"
echo ""
echo "서버 시작 후 다음 URL로 접속하세요:"
echo "  - API 문서: http://localhost:3000/docs"
echo "  - 서버 상태: http://localhost:3000/health"
echo ""
echo "테스트 클라이언트 실행:"
echo "  ${GREEN}python test_client.py${NC}"
echo ""

