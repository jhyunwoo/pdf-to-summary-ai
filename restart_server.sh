#!/bin/bash

echo "🔄 서버 재시작 스크립트"
echo "=" * 60

# 기존 서버 프로세스 종료
echo "🛑 기존 서버 프로세스 종료 중..."
pkill -9 -f "python server.py" 2>/dev/null
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

# 가상환경 활성화 및 서버 시작
source venv/bin/activate

# 서버 시작 (포그라운드로 - 에러 확인용)
python server.py

# 백그라운드로 시작하려면 아래 사용:
# nohup python server.py > server.log 2>&1 &
# echo "✅ 서버가 백그라운드에서 시작되었습니다! (PID: $!)"
# echo "📊 로그 확인: tail -f server.log"

