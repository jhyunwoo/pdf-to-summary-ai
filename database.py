"""
Database connection and session management
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv("DB_URL", "sqlite:///./analysis_records.db")

# SQLAlchemy 엔진 생성 (PostgreSQL 연결 풀 설정)
if "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL:
    # PostgreSQL 연결 풀 설정
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,  # 연결 풀 크기
        max_overflow=20,  # 추가 연결 허용
        pool_pre_ping=True,  # 연결 유효성 검사 (자동 재연결)
        pool_recycle=3600,  # 1시간마다 연결 재생성
        echo=False  # SQL 쿼리 로깅 (개발 시 True로 설정 가능)
    )
else:
    # SQLite 설정
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

# 세션 로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 (모든 모델이 상속받을 베이스)
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 의존성
    FastAPI의 Depends에서 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    데이터베이스 초기화
    모든 테이블 생성
    """
    from models import AnalysisRecord  # 순환 import 방지
    Base.metadata.create_all(bind=engine)

