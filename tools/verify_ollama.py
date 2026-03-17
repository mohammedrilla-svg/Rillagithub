
import requests
import json
import sys

def verify_ollama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2",
        "prompt": "Say 'Connection Successful' if you can read this.",
        "stream": False
    }
    
    print(f"Testing connection to {url} with model 'llama3.2'...")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        actual_response = data.get('response', '').strip()
        print(f"Received response: {actual_response}")
        
        if "Connection Successful" in actual_response:
            print("✅ Handshake Verified: Ollama is running and responding.")
            return True
        else:
            print(f"⚠️  Ollama responded, but message was unexpected: {actual_response}")
            return True # Still strictly a connection success
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Failed: Could not connect to localhost:11434. Is 'ollama serve' running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = verify_ollama()
    if not success:
        sys.exit(1)
