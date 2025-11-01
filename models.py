"""
Database models for storing analysis records
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base


class AnalysisRecord(Base):
    """
    분석 요청과 결과를 저장하는 모델
    """
    __tablename__ = "analysis_records"

    # 기본 필드
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 요청 정보
    endpoint = Column(String(100), nullable=False, index=True)  # API 엔드포인트
    prompt = Column(Text, nullable=False)  # 입력 프롬프트
    has_image = Column(Boolean, default=False)  # 이미지 포함 여부
    image_filename = Column(String(255))  # 이미지 파일명 (있는 경우)
    
    # 생성 옵션
    temperature = Column(Float)
    max_tokens = Column(Integer)
    
    # 응답 정보
    response = Column(Text)  # 모델의 응답
    model = Column(String(100))  # 사용된 모델명
    success = Column(Boolean, default=True)  # 성공 여부
    error_message = Column(Text)  # 에러 메시지 (실패 시)
    
    # 성능 메트릭
    total_duration = Column(Integer)  # 총 처리 시간 (나노초)
    load_duration = Column(Integer)  # 모델 로드 시간 (나노초)
    prompt_eval_count = Column(Integer)  # 프롬프트 평가 토큰 수
    eval_count = Column(Integer)  # 생성된 토큰 수
    
    def __repr__(self):
        return f"<AnalysisRecord(id={self.id}, endpoint='{self.endpoint}', created_at='{self.created_at}')>"
    
    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "endpoint": self.endpoint,
            "prompt": self.prompt,
            "has_image": self.has_image,
            "image_filename": self.image_filename,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response": self.response,
            "model": self.model,
            "success": self.success,
            "error_message": self.error_message,
            "total_duration": self.total_duration,
            "load_duration": self.load_duration,
            "prompt_eval_count": self.prompt_eval_count,
            "eval_count": self.eval_count,
        }

