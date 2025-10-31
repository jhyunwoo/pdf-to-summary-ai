"""
Ollama Qwen3-VL API Server
이미지와 프롬프트를 입력받아 ollama의 qwen3-vl:235b 모델로 처리하는 서버
"""
import os
import base64
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import json
from io import BytesIO
from PIL import Image

app = FastAPI(
    title="Ollama Qwen3-VL API Server",
    description="이미지와 프롬프트를 처리하는 Vision Language Model 서버",
    version="1.0.0"
)

# Ollama API 설정
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3-vl:235b")


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
        "message": "Ollama Qwen3-VL API Server",
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


@app.post("/api/generate")
async def generate_with_image(
    image: UploadFile = File(..., description="입력 이미지 파일"),
    prompt: str = Form(..., description="처리할 프롬프트"),
    temperature: float = Form(0.7, description="생성 온도 (0.0-1.0)"),
    max_tokens: int = Form(2000, description="최대 토큰 수")
):
    """
    이미지와 프롬프트를 받아서 Qwen3-VL 모델로 처리
    
    Args:
        image: 업로드된 이미지 파일
        prompt: 처리할 텍스트 프롬프트
        temperature: 생성 온도 (낮을수록 결정적, 높을수록 창의적)
        max_tokens: 생성할 최대 토큰 수
    
    Returns:
        모델의 응답 텍스트
    """
    try:
        # 이미지 읽기
        image_bytes = await image.read()
        
        # 이미지 유효성 검증
        if not validate_image(image_bytes):
            raise HTTPException(status_code=400, detail="유효하지 않은 이미지 형식입니다.")
        
        # 이미지를 base64로 인코딩
        image_base64 = encode_image_to_base64(image_bytes)
        
        # Ollama API 요청 준비
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        # Ollama API 호출
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=300  # 5분 타임아웃 (큰 모델이므로)
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ollama API 오류: {response.text}"
            )
        
        result = response.json()
        
        return {
            "success": True,
            "response": result.get("response", ""),
            "model": MODEL_NAME,
            "prompt": prompt,
            "done": result.get("done", False),
            "context": result.get("context", []),
            "total_duration": result.get("total_duration"),
            "load_duration": result.get("load_duration"),
            "prompt_eval_count": result.get("prompt_eval_count"),
            "eval_count": result.get("eval_count")
        }
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Ollama 서버 응답 시간 초과")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama 서버에 연결할 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.post("/api/generate/text")
async def generate_text_only(request: TextPromptRequest):
    """
    텍스트만 처리 (이미지 없이)
    
    Args:
        request: 프롬프트와 생성 옵션을 포함한 요청
    
    Returns:
        모델의 응답 텍스트
    """
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
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ollama API 오류: {response.text}"
            )
        
        result = response.json()
        
        return {
            "success": True,
            "response": result.get("response", ""),
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "done": result.get("done", False)
        }
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Ollama 서버 응답 시간 초과")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama 서버에 연결할 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.post("/api/generate/stream")
async def generate_with_image_stream(
    image: UploadFile = File(..., description="입력 이미지 파일"),
    prompt: str = Form(..., description="처리할 프롬프트"),
    temperature: float = Form(0.7, description="생성 온도 (0.0-1.0)"),
):
    """
    이미지와 프롬프트를 받아서 스트리밍 방식으로 응답
    (실시간으로 결과를 받아볼 수 있음)
    """
    try:
        from fastapi.responses import StreamingResponse
        
        # 이미지 읽기
        image_bytes = await image.read()
        
        # 이미지 유효성 검증
        if not validate_image(image_bytes):
            raise HTTPException(status_code=400, detail="유효하지 않은 이미지 형식입니다.")
        
        # 이미지를 base64로 인코딩
        image_base64 = encode_image_to_base64(image_bytes)
        
        # Ollama API 요청 준비
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "images": [image_base64],
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }
        
        def generate():
            """스트리밍 응답 생성"""
            try:
                response = requests.post(
                    f"{OLLAMA_HOST}/api/generate",
                    json=payload,
                    stream=True,
                    timeout=300
                )
                
                for line in response.iter_lines():
                    if line:
                        yield line + b'\n'
            except Exception as e:
                yield json.dumps({"error": str(e)}).encode() + b'\n'
        
        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 3000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Ollama Qwen3-VL API Server 시작")
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

