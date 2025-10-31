"""
Ollama Qwen3-VL API 사용 예제
"""
import requests
import json
from pathlib import Path


def example_1_text_only():
    """예제 1: 텍스트만 처리"""
    print("=" * 60)
    print("예제 1: 텍스트만 처리")
    print("=" * 60)
    
    url = "http://localhost:8000/api/generate/text"
    
    payload = {
        "prompt": "인공지능이란 무엇인가요?",
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    print(f"📝 요청: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print("\n⏳ 응답 대기 중...\n")
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 성공!")
            print(f"\n응답:\n{result['response']}")
        else:
            print(f"❌ 오류: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print("\n")


def example_2_image_analysis(image_path: str):
    """예제 2: 이미지 분석"""
    print("=" * 60)
    print("예제 2: 이미지 분석")
    print("=" * 60)
    
    if not Path(image_path).exists():
        print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        return
    
    url = "http://localhost:8000/api/generate"
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {
            "prompt": "이 이미지에 대해 자세히 설명해주세요.",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        print(f"🖼️  이미지: {image_path}")
        print(f"📝 프롬프트: {data['prompt']}")
        print("\n⏳ 응답 대기 중...\n")
        
        try:
            response = requests.post(url, files=files, data=data, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 성공!")
                print(f"\n응답:\n{result['response']}")
                print(f"\n📊 메타데이터:")
                print(f"  - 프롬프트 토큰: {result.get('prompt_eval_count')}")
                print(f"  - 생성 토큰: {result.get('eval_count')}")
            else:
                print(f"❌ 오류: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    print("\n")


def example_3_image_qa(image_path: str):
    """예제 3: 이미지 Q&A"""
    print("=" * 60)
    print("예제 3: 이미지 Q&A")
    print("=" * 60)
    
    if not Path(image_path).exists():
        print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        return
    
    url = "http://localhost:8000/api/generate"
    
    questions = [
        "이 이미지에 무엇이 보이나요?",
        "이미지의 색상은 무엇인가요?",
        "이 이미지에서 가장 눈에 띄는 것은 무엇인가요?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n질문 {i}: {question}")
        
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {
                "prompt": question,
                "temperature": 0.5,
                "max_tokens": 200
            }
            
            try:
                response = requests.post(url, files=files, data=data, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"답변: {result['response']}")
                else:
                    print(f"❌ 오류: {response.status_code}")
            
            except Exception as e:
                print(f"❌ 오류: {e}")
    
    print("\n")


def example_4_document_ocr(image_path: str):
    """예제 4: 문서 OCR (텍스트 추출)"""
    print("=" * 60)
    print("예제 4: 문서 OCR")
    print("=" * 60)
    
    if not Path(image_path).exists():
        print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        return
    
    url = "http://localhost:8000/api/generate"
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {
            "prompt": "이 이미지에 있는 모든 텍스트를 정확하게 추출해주세요.",
            "temperature": 0.1,  # 정확성을 위해 낮은 온도
            "max_tokens": 2000
        }
        
        print(f"🖼️  이미지: {image_path}")
        print(f"📝 프롬프트: {data['prompt']}")
        print("\n⏳ 응답 대기 중...\n")
        
        try:
            response = requests.post(url, files=files, data=data, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 성공!")
                print(f"\n추출된 텍스트:\n{result['response']}")
            else:
                print(f"❌ 오류: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    print("\n")


def example_5_multi_turn_conversation(image_path: str):
    """예제 5: 다중 턴 대화 (컨텍스트 유지)"""
    print("=" * 60)
    print("예제 5: 다중 턴 대화")
    print("=" * 60)
    
    if not Path(image_path).exists():
        print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        return
    
    url = "http://localhost:8000/api/generate"
    
    # 첫 번째 질문
    print("\n👤 사용자: 이 이미지에 대해 설명해주세요.")
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {
            "prompt": "이 이미지에 대해 설명해주세요.",
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, files=files, data=data, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                context = result.get("context", [])
                print(f"🤖 AI: {result['response']}")
                
                # 두 번째 질문 (컨텍스트 포함)
                print("\n👤 사용자: 더 자세히 설명해주세요.")
                
                # 주의: Ollama API는 컨텍스트를 별도로 관리해야 함
                # 실제 구현에서는 서버 측에서 세션 관리가 필요
                
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    print("\n")


def main():
    """메인 함수"""
    print("\n🚀 Ollama Qwen3-VL API 사용 예제\n")
    
    # 예제 1: 텍스트만 처리
    example_1_text_only()
    
    # 이미지가 있는 경우 나머지 예제 실행
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        # 예제 2: 이미지 분석
        example_2_image_analysis(image_path)
        
        # 예제 3: 이미지 Q&A
        example_3_image_qa(image_path)
        
        # 예제 4: 문서 OCR
        # example_4_document_ocr(image_path)
        
        # 예제 5: 다중 턴 대화
        # example_5_multi_turn_conversation(image_path)
    else:
        print("💡 이미지 예제를 실행하려면:")
        print("   python example_usage.py <이미지_경로>")
        print("\n예시:")
        print("   python example_usage.py example.jpg")
    
    print("\n✨ 예제 실행 완료!\n")


if __name__ == "__main__":
    main()

