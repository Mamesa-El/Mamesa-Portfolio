import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ Health check passed!")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print("-" * 50)

def test_chat(system_prompt="You are a helpful assistant.", user_message="Tell me a short joke."):
    """Test the chat endpoint with a simple request"""
    print("\n🔍 Testing chat endpoint...")
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }
    
    try:
        print(f"Request payload: {json.dumps(data, indent=2)}")
        start_time = time.time()
        response = requests.post(f"{API_URL}/chat", json=data)
        end_time = time.time()
        
        print(f"Status code: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Model: {result.get('model', 'unknown')}")
            print(f"Response: {result.get('response', '')}")
            print("✅ Chat test passed!")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print("-" * 50)

def test_streaming_chat():
    """Test the streaming chat endpoint"""
    print("\n🔍 Testing streaming chat endpoint...")
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Count from 1 to 5 slowly."}
        ],
        "temperature": 0.7,
        "max_tokens": 300,
        "stream": True
    }
    
    try:
        print("Initiating streaming request...")
        response = requests.post(
            f"{API_URL}/stream-chat", 
            json=data,
            stream=True
        )
        
        if response.status_code == 200:
            print("Stream started (showing first few chunks):")
            chunk_count = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data:'):
                        data_str = line_str[5:].strip()
                        if data_str == "[DONE]":
                            print("Stream completed.")
                            break
                        try:
                            data_json = json.loads(data_str)
                            if 'text' in data_json:
                                print(f"Chunk {chunk_count}: {data_json['text']}")
                        except json.JSONDecodeError:
                            print(f"Could not decode: {data_str}")
                    chunk_count += 1
                    if chunk_count > 5:
                        print("... (more chunks available) ...")
                        break
            print("✅ Streaming test passed!")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    print("-" * 50)

def run_custom_test(system_prompt, user_message):
    """Run a custom test with user-provided prompts"""
    print("\n🔍 Running custom test...")
    test_chat(system_prompt, user_message)

if __name__ == "__main__":
    print("=== 🤖 Testing Ollama FastAPI Wrapper ===")
    
    # Run basic tests
    test_health()
    test_chat()
    test_streaming_chat()
    
    # Optional: Run a custom test
    print("\nWould you like to run a custom test? (y/n)")
    if input().lower() == 'y':
        print("Enter system prompt:")
        system_prompt = input()
        print("Enter user message:")
        user_message = input()
        run_custom_test(system_prompt, user_message)
    
    print("\n=== 🏁 Testing completed ===")