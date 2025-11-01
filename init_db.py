#!/usr/bin/env python3
"""
데이터베이스 스키마 초기화 스크립트
서버를 실행하지 않고 데이터베이스 테이블만 생성합니다.
"""
import sys
from database import init_db, engine, DATABASE_URL
from sqlalchemy import inspect, text

def check_tables_exist():
    """현재 존재하는 테이블 확인"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return tables

def print_table_schema():
    """테이블 스키마 출력"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if not tables:
        print("⚠️  테이블이 없습니다.")
        return
    
    for table_name in tables:
        print(f"\n📋 테이블: {table_name}")
        print("-" * 60)
        columns = inspector.get_columns(table_name)
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"  - {col['name']:<20} {str(col['type']):<20} {nullable}")
        
        # 인덱스 정보
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\n  인덱스:")
            for idx in indexes:
                print(f"    - {idx['name']}: {idx['column_names']}")

def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("📊 데이터베이스 스키마 초기화")
    print("=" * 70)
    print(f"\n🔗 데이터베이스 URL: {DATABASE_URL}\n")
    
    # 기존 테이블 확인
    existing_tables = check_tables_exist()
    
    if existing_tables:
        print(f"✅ 기존 테이블 발견: {', '.join(existing_tables)}\n")
        response = input("기존 테이블을 유지하고 계속하시겠습니까? (y/N): ").strip().lower()
        
        if response != 'y':
            print("\n❌ 취소되었습니다.")
            sys.exit(0)
    else:
        print("📝 테이블이 없습니다. 새로 생성합니다.\n")
    
    try:
        # 데이터베이스 초기화
        print("🔧 스키마 적용 중...")
        init_db()
        print("✅ 스키마 적용 완료!\n")
        
        # 생성된 테이블 확인
        print("=" * 70)
        print_table_schema()
        print("\n" + "=" * 70)
        
        # 테이블 수 카운트
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM analysis_records"))
            count = result.scalar()
            print(f"\n📊 현재 저장된 레코드 수: {count}")
        
        print("\n✨ 데이터베이스 준비 완료!")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

