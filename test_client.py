"""
Ollama Gemma3 API 서버 테스트 클라이언트
"""
import requests
import json
import sys
from pathlib import Path


# API 서버 URL
API_BASE_URL = "http://165.132.141.231:30942"


def test_server_status():
    """서버 상태 확인 테스트"""
    print("=" * 50)
    print("서버 상태 확인 테스트")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ 서버 응답: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()


def test_health_check():
    """헬스체크 테스트"""
    print("=" * 50)
    print("헬스체크 테스트")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"✅ 응답: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()


def test_text_only(prompt: str):
    """텍스트만 처리 테스트"""
    print("=" * 50)
    print("텍스트 처리 테스트")
    print("=" * 50)
    
    try:
        url = f"{API_BASE_URL}/api/generate/text"
        payload = {
            "prompt": prompt,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        print(f"📝 프롬프트: {prompt}")
        print("⏳ 응답 대기 중...")
        
        response = requests.post(url, json=payload, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 성공!")
            print(f"\n🤖 모델 응답:")
            print("-" * 50)
            print(result.get("response", ""))
            print("-" * 50)
            print(f"\n📊 메타데이터:")
            print(f"  - 모델: {result.get('model')}")
            print(f"  - 완료: {result.get('done')}")
        else:
            print(f"❌ 오류: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()


def test_image_with_prompt(image_path: str, prompt: str):
    """이미지 + 프롬프트 처리 테스트"""
    print("=" * 50)
    print("이미지 + 프롬프트 처리 테스트")
    print("=" * 50)
    
    # 이미지 파일 확인
    image_file = Path(image_path)
    if not image_file.exists():
        print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        return
    
    try:
        url = f"{API_BASE_URL}/api/generate"
        
        with open(image_path, "rb") as f:
            files = {"image": (image_file.name, f, "image/jpeg")}
            data = {
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            print(f"🖼️  이미지: {image_path}")
            print(f"📝 프롬프트: {prompt}")
            print("⏳ 응답 대기 중 (시간이 걸릴 수 있습니다)...")
            
            response = requests.post(url, files=files, data=data, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 성공!")
                print(f"\n🤖 모델 응답:")
                print("-" * 50)
                print(result.get("response", ""))
                print("-" * 50)
                print(f"\n📊 메타데이터:")
                print(f"  - 모델: {result.get('model')}")
                print(f"  - 완료: {result.get('done')}")
                print(f"  - 프롬프트 토큰: {result.get('prompt_eval_count')}")
                print(f"  - 생성 토큰: {result.get('eval_count')}")
            else:
                print(f"❌ 오류: {response.status_code}")
                print(response.text)
    
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()


def test_streaming(image_path: str, prompt: str):
    """스트리밍 응답 테스트"""
    print("=" * 50)
    print("스트리밍 응답 테스트")
    print("=" * 50)
    
    # 이미지 파일 확인
    image_file = Path(image_path)
    if not image_file.exists():
        print(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
        return
    
    try:
        url = f"{API_BASE_URL}/api/generate/stream"
        
        with open(image_path, "rb") as f:
            files = {"image": (image_file.name, f, "image/jpeg")}
            data = {
                "prompt": prompt,
                "temperature": 0.7
            }
            
            print(f"🖼️  이미지: {image_path}")
            print(f"📝 프롬프트: {prompt}")
            print("⏳ 스트리밍 응답 수신 중...")
            print("-" * 50)
            
            response = requests.post(url, files=files, data=data, stream=True, timeout=300)
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "response" in data:
                                print(data["response"], end="", flush=True)
                        except json.JSONDecodeError:
                            pass
                print()
                print("-" * 50)
                print("✅ 스트리밍 완료!")
            else:
                print(f"❌ 오류: {response.status_code}")
                print(response.text)
    
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    print()


def main():
    """메인 함수"""
    print("\n🚀 Ollama Qwen3-VL API 테스트 클라이언트\n")
    
    # 1. 서버 상태 확인
    test_server_status()
    
    # 2. 헬스체크
    test_health_check()
    
    # 3. 텍스트 처리 테스트
    # test_text_only("Please describe about linux kernel.")
    
    # 4. 이미지 + 프롬프트 테스트 (이미지 파일이 있는 경우)
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        prompt = sys.argv[2] if len(sys.argv) > 2 else "이 이미지에 대해 자세히 설명해주세요."
        
        test_image_with_prompt(image_path, prompt)
        
        # 5. 스트리밍 테스트
        # test_streaming(image_path, "이 이미지를 분석해주세요.")
    else:
        print("💡 이미지 테스트를 하려면 다음과 같이 실행하세요:")
        print("   python test_client.py <이미지_경로> [프롬프트]")
        print("\n예시:")
        print("   python test_client.py test.jpg \"이 이미지에 무엇이 있나요?\"")
    
    print("\n✨ 테스트 완료!\n")


if __name__ == "__main__":
    main()


