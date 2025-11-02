"""
데이터베이스 마이그레이션: image_url 컬럼 추가
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def migrate_database():
    """image_url 컬럼을 analysis_records 테이블에 추가"""
    
    # 데이터베이스 URL 가져오기
    database_url = os.getenv("DB_URL")
    
    if not database_url:
        print("⚠️  DATABASE_URL 환경 변수가 설정되지 않았습니다.")
        print("기본 SQLite 데이터베이스를 사용합니다.")
        database_url = "sqlite:///./analysis_records.db"
    
    print(f"🔗 데이터베이스 연결: {database_url}")
    
    # 엔진 생성
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            # 컬럼 존재 여부 확인
            if "postgresql" in database_url or "postgres" in database_url:
                # PostgreSQL
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='analysis_records' AND column_name='image_url'
                """))
                
                if result.fetchone():
                    print("✅ image_url 컬럼이 이미 존재합니다.")
                    return
                
                # 컬럼 추가
                conn.execute(text("ALTER TABLE analysis_records ADD COLUMN image_url TEXT"))
                conn.commit()
                print("✅ PostgreSQL: image_url 컬럼 추가 완료")
                
            elif "sqlite" in database_url:
                # SQLite
                result = conn.execute(text("PRAGMA table_info(analysis_records)"))
                columns = [row[1] for row in result.fetchall()]
                
                if 'image_url' in columns:
                    print("✅ image_url 컬럼이 이미 존재합니다.")
                    return
                
                # 컬럼 추가
                conn.execute(text("ALTER TABLE analysis_records ADD COLUMN image_url TEXT"))
                conn.commit()
                print("✅ SQLite: image_url 컬럼 추가 완료")
            
            else:
                print("⚠️  지원하지 않는 데이터베이스 타입입니다.")
                return
            
            print("✨ 마이그레이션 완료!")
            
    except Exception as e:
        print(f"❌ 마이그레이션 실패: {e}")
        print("\n만약 테이블이 존재하지 않는다면, 먼저 init_db.py를 실행하세요:")
        print("  python init_db.py")


if __name__ == "__main__":
    print("\n🔧 데이터베이스 마이그레이션 시작\n")
    migrate_database()
    print()

