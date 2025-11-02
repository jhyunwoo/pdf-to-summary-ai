"""
데이터베이스 마이그레이션: Integer → BigInteger 변경
total_duration과 load_duration 컬럼의 타입을 변경하여 integer overflow 문제 해결
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def migrate_database():
    """total_duration과 load_duration 컬럼을 Integer에서 BigInteger로 변경"""
    
    # 데이터베이스 URL 가져오기
    database_url = os.getenv("DB_URL")
    
    if not database_url:
        print("⚠️  DB_URL 환경 변수가 설정되지 않았습니다.")
        print("기본 SQLite 데이터베이스를 사용합니다.")
        database_url = "sqlite:///./analysis_records.db"
    
    print(f"🔗 데이터베이스 연결: {database_url}")
    
    # 엔진 생성
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            if "postgresql" in database_url or "postgres" in database_url:
                print("📊 PostgreSQL 데이터베이스 감지")
                
                # total_duration 컬럼 타입 변경
                print("🔧 total_duration 컬럼 타입 변경 중...")
                conn.execute(text("""
                    ALTER TABLE analysis_records 
                    ALTER COLUMN total_duration TYPE BIGINT
                """))
                
                # load_duration 컬럼 타입 변경
                print("🔧 load_duration 컬럼 타입 변경 중...")
                conn.execute(text("""
                    ALTER TABLE analysis_records 
                    ALTER COLUMN load_duration TYPE BIGINT
                """))
                
                conn.commit()
                print("✅ PostgreSQL: 컬럼 타입 변경 완료")
                
            elif "sqlite" in database_url:
                print("📊 SQLite 데이터베이스 감지")
                print("ℹ️  SQLite는 동적 타이핑을 사용하므로 별도 마이그레이션이 필요하지 않습니다.")
                print("✅ SQLite: 변경 사항 없음")
            
            else:
                print("⚠️  지원하지 않는 데이터베이스 타입입니다.")
                return
            
            print("\n✨ 마이그레이션 완료!")
            print("\n📝 변경 내용:")
            print("  - total_duration: INTEGER → BIGINT")
            print("  - load_duration: INTEGER → BIGINT")
            print("\n이제 서버를 재시작하세요:")
            print("  ./restart_server.sh")
            
    except Exception as e:
        print(f"❌ 마이그레이션 실패: {e}")
        print("\n문제 해결 방법:")
        print("1. 데이터베이스 연결 정보를 확인하세요")
        print("2. analysis_records 테이블이 존재하는지 확인하세요")
        print("3. 데이터베이스 사용자 권한을 확인하세요")
        return False
    
    return True


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔧 Integer Overflow 문제 해결 마이그레이션")
    print("=" * 60)
    print("\n문제: total_duration과 load_duration 값이 Integer 범위 초과")
    print("해결: INTEGER → BIGINT로 타입 변경\n")
    
    success = migrate_database()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 마이그레이션 성공!")
        print("=" * 60 + "\n")
    else:
        print("\n" + "=" * 60)
        print("❌ 마이그레이션 실패")
        print("=" * 60 + "\n")

