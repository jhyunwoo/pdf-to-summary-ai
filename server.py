"""
Ollama Gemma3 API Server
텍스트 프롬프트를 입력받아 ollama의 gemma3:27b 모델로 처리하는 서버
"""
import os
import base64
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import json
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# 환경 변수 로드
load_dotenv()

# DB 관련 import
from database import get_db, init_db
from models import AnalysisRecord


# 최신 FastAPI lifespan 이벤트 핸들러
@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # Startup
    try:
        print("🔧 데이터베이스 초기화 중...")
        init_db()
        print("✅ 데이터베이스 초기화 완료")
    except Exception as e:
        print(f"⚠️  데이터베이스 초기화 실패: {e}")
        print("⚠️  DB 기능 없이 서버를 시작합니다. DB 설정을 확인하세요.")
    
    yield
    
    # Shutdown
    print("🛑 서버 종료 중...")


app = FastAPI(
    title="Ollama Gemma3 API Server",
    description="텍스트 프롬프트를 처리하는 Language Model 서버",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정 - 모든 origin 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# Ollama API 설정
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:27b")


class TextPromptRequest(BaseModel):
    """텍스트만 처리하는 요청"""
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000


def encode_image_to_base64(image_bytes: bytes) -> str:
    """이미지를 base64로 인코딩"""
    return base64.b64encode(image_bytes).decode('utf-8')


def validate_image(image_bytes: bytes) -> bool:
    """이미지 유효성 검증"""
    try:
        img = Image.open(BytesIO(image_bytes))
        img.verify()
        return True
    except Exception:
        return False


@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "status": "running",
        "message": "Ollama Gemma3 API Server",
        "model": MODEL_NAME,
        "ollama_host": OLLAMA_HOST
    }


@app.get("/health")
async def health_check():
    """헬스체크 및 ollama 연결 확인"""
    try:
        # Ollama 서버 연결 확인
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_exists = any(MODEL_NAME in model.get("name", "") for model in models)
            
            return {
                "status": "healthy",
                "ollama_connected": True,
                "model_loaded": model_exists,
                "available_models": [model.get("name") for model in models]
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "ollama_connected": False,
                    "error": "Ollama server is not responding properly"
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "ollama_connected": False,
                "error": str(e)
            }
        )


class ImageUrlRequest(BaseModel):
    """이미지 URL로 요청하는 모델"""
    image_url: str
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000


def download_image_from_url(url: str) -> bytes:
    """URL에서 이미지를 다운로드"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 다운로드 실패: {str(e)}")


@app.post("/api/generate")
async def generate_with_image(request: ImageUrlRequest, db: Session = Depends(get_db)):
    """
    이미지 URL과 프롬프트를 받아서 Gemma3 모델로 처리
    
    Args:
        request: 이미지 URL, 프롬프트, 생성 옵션을 포함한 요청
        db: 데이터베이스 세션
    
    Returns:
        모델의 응답 텍스트
    """
    # DB 레코드 초기화
    record = AnalysisRecord(
        endpoint="/api/generate",
        prompt=request.prompt,
        has_image=True,
        image_url=request.image_url,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        model=MODEL_NAME
    )
    
    try:
        # URL에서 이미지 다운로드
        image_bytes = download_image_from_url(request.image_url)
        
        # 이미지 유효성 검증
        if not validate_image(image_bytes):
            record.success = False
            record.error_message = "유효하지 않은 이미지 형식입니다."
            db.add(record)
            db.commit()
            raise HTTPException(status_code=400, detail="유효하지 않은 이미지 형식입니다.")
        
        # 이미지를 base64로 인코딩
        image_base64 = encode_image_to_base64(image_bytes)
        
        # Ollama API 요청 준비
        payload = {
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "images": [image_base64],
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            }
        }
        
        # Ollama API 호출
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=300  # 5분 타임아웃 (큰 모델이므로)
        )
        
        if response.status_code != 200:
            record.success = False
            record.error_message = f"Ollama API 오류: {response.text}"
            db.add(record)
            db.commit()
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ollama API 오류: {response.text}"
            )
        
        result = response.json()
        
        # DB에 성공 결과 저장
        record.response = result.get("response", "")
        record.success = True
        record.total_duration = result.get("total_duration")
        record.load_duration = result.get("load_duration")
        record.prompt_eval_count = result.get("prompt_eval_count")
        record.eval_count = result.get("eval_count")
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return {
            "success": True,
            "response": result.get("response", ""),
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "done": result.get("done", False),
            "context": result.get("context", []),
            "total_duration": result.get("total_duration"),
            "load_duration": result.get("load_duration"),
            "prompt_eval_count": result.get("prompt_eval_count"),
            "eval_count": result.get("eval_count"),
            "record_id": record.id  # DB 레코드 ID 추가
        }
        
    except requests.exceptions.Timeout:
        record.success = False
        record.error_message = "Ollama 서버 응답 시간 초과"
        db.add(record)
        db.commit()
        raise HTTPException(status_code=504, detail="Ollama 서버 응답 시간 초과")
    except requests.exceptions.ConnectionError:
        record.success = False
        record.error_message = "Ollama 서버에 연결할 수 없습니다."
        db.add(record)
        db.commit()
        raise HTTPException(status_code=503, detail="Ollama 서버에 연결할 수 없습니다.")
    except HTTPException:
        # HTTPException은 이미 처리됨
        raise
    except Exception as e:
        record.success = False
        record.error_message = str(e)
        db.add(record)
        db.commit()
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.post("/api/generate/text")
async def generate_text_only(request: TextPromptRequest, db: Session = Depends(get_db)):
    """
    텍스트만 처리 (이미지 없이)
    
    Args:
        request: 프롬프트와 생성 옵션을 포함한 요청
        db: 데이터베이스 세션
    
    Returns:
        모델의 응답 텍스트
    """
    # DB 레코드 초기화
    record = AnalysisRecord(
        endpoint="/api/generate/text",
        prompt=request.prompt,
        has_image=False,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        model=MODEL_NAME
    )
    
    try:
        # Ollama API 요청 준비
        payload = {
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            }
        }
        
        # Ollama API 호출
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=300
        )
        
        if response.status_code != 200:
            record.success = False
            record.error_message = f"Ollama API 오류: {response.text}"
            db.add(record)
            db.commit()
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ollama API 오류: {response.text}"
            )
        
        result = response.json()
        
        # DB에 성공 결과 저장
        record.response = result.get("response", "")
        record.success = True
        record.total_duration = result.get("total_duration")
        record.load_duration = result.get("load_duration")
        record.prompt_eval_count = result.get("prompt_eval_count")
        record.eval_count = result.get("eval_count")
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return {
            "success": True,
            "response": result.get("response", ""),
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "done": result.get("done", False),
            "record_id": record.id  # DB 레코드 ID 추가
        }
        
    except requests.exceptions.Timeout:
        record.success = False
        record.error_message = "Ollama 서버 응답 시간 초과"
        db.add(record)
        db.commit()
        raise HTTPException(status_code=504, detail="Ollama 서버 응답 시간 초과")
    except requests.exceptions.ConnectionError:
        record.success = False
        record.error_message = "Ollama 서버에 연결할 수 없습니다."
        db.add(record)
        db.commit()
        raise HTTPException(status_code=503, detail="Ollama 서버에 연결할 수 없습니다.")
    except HTTPException:
        # HTTPException은 이미 처리됨
        raise
    except Exception as e:
        record.success = False
        record.error_message = str(e)
        db.add(record)
        db.commit()
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.get("/api/records")
async def get_analysis_records(
    skip: int = 0,
    limit: int = 100,
    endpoint: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    저장된 분석 기록 조회
    
    Args:
        skip: 건너뛸 레코드 수
        limit: 가져올 최대 레코드 수
        endpoint: 특정 엔드포인트로 필터링 (선택사항)
        db: 데이터베이스 세션
    
    Returns:
        분석 기록 목록
    """
    query = db.query(AnalysisRecord)
    
    if endpoint:
        query = query.filter(AnalysisRecord.endpoint == endpoint)
    
    records = query.order_by(AnalysisRecord.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "total": query.count(),
        "records": [record.to_dict() for record in records]
    }


@app.get("/api/records/{record_id}")
async def get_analysis_record(record_id: int, db: Session = Depends(get_db)):
    """
    특정 분석 기록 조회
    
    Args:
        record_id: 조회할 레코드 ID
        db: 데이터베이스 세션
    
    Returns:
        분석 기록 상세 정보
    """
    record = db.query(AnalysisRecord).filter(AnalysisRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="레코드를 찾을 수 없습니다.")
    
    return {
        "success": True,
        "record": record.to_dict()
    }


class ImageUrlStreamRequest(BaseModel):
    """이미지 URL 스트리밍 요청 모델"""
    image_url: str
    prompt: str
    temperature: Optional[float] = 0.7


@app.post("/api/generate/stream")
async def generate_with_image_stream(request: ImageUrlStreamRequest, db: Session = Depends(get_db)):
    """
    이미지 URL과 프롬프트를 받아서 스트리밍 방식으로 응답
    (실시간으로 결과를 받아볼 수 있음)
    """
    # DB 레코드 초기화
    record = AnalysisRecord(
        endpoint="/api/generate/stream",
        prompt=request.prompt,
        has_image=True,
        image_url=request.image_url,
        temperature=request.temperature,
        model=MODEL_NAME
    )
    
    try:
        from fastapi.responses import StreamingResponse
        
        # URL에서 이미지 다운로드
        image_bytes = download_image_from_url(request.image_url)
        
        # 이미지 유효성 검증
        if not validate_image(image_bytes):
            record.success = False
            record.error_message = "유효하지 않은 이미지 형식입니다."
            db.add(record)
            db.commit()
            raise HTTPException(status_code=400, detail="유효하지 않은 이미지 형식입니다.")
        
        # 이미지를 base64로 인코딩
        image_base64 = encode_image_to_base64(image_bytes)
        
        # Ollama API 요청 준비
        payload = {
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "images": [image_base64],
            "stream": True,
            "options": {
                "temperature": request.temperature
            }
        }
        
        def generate():
            """스트리밍 응답 생성 및 DB에 저장"""
            full_response = []
            last_metrics = {}
            
            try:
                response = requests.post(
                    f"{OLLAMA_HOST}/api/generate",
                    json=payload,
                    stream=True,
                    timeout=300
                )
                
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk_data = json.loads(line)
                            # 응답 텍스트 수집
                            if "response" in chunk_data:
                                full_response.append(chunk_data["response"])
                            # 메트릭 정보 수집
                            if chunk_data.get("done"):
                                last_metrics = chunk_data
                        except json.JSONDecodeError:
                            pass
                        
                        yield line + b'\n'
                
                # 스트리밍 완료 후 DB에 저장
                record.response = "".join(full_response)
                record.success = True
                record.total_duration = last_metrics.get("total_duration")
                record.load_duration = last_metrics.get("load_duration")
                record.prompt_eval_count = last_metrics.get("prompt_eval_count")
                record.eval_count = last_metrics.get("eval_count")
                db.add(record)
                db.commit()
                
            except Exception as e:
                record.success = False
                record.error_message = str(e)
                record.response = "".join(full_response) if full_response else None
                db.add(record)
                db.commit()
                yield json.dumps({"error": str(e)}).encode() + b'\n'
        
        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        record.success = False
        record.error_message = str(e)
        db.add(record)
        db.commit()
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 3000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Ollama Gemma3 API Server 시작")
    print(f"📍 서버 주소: http://{host}:{port}")
    print(f"🤖 모델: {MODEL_NAME}")
    print(f"🔗 Ollama 호스트: {OLLAMA_HOST}")
    print(f"📚 API 문서: http://{host}:{port}/docs")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

