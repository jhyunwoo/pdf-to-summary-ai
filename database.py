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

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # SQL 쿼리 로깅 (개발 시 True로 설정 가능)
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

