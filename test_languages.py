import requests
import json

# Test multi-language code generation
url = "http://localhost:8000/api/v1/generate-code"

languages = ["python", "javascript", "java", "cpp", "c"]
prompt = "factorial program"

print("Testing Multi-Language Code Generation")
print("=" * 50)

for lang in languages:
    data = {
        "prompt": prompt,
        "language": lang
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            code = result.get('generated_code', 'No code generated')
            
            print(f"\n{lang.upper()}:")
            print("-" * 30)
            # Show first few lines of code
            lines = code.split('\n')[:5]
            for line in lines:
                print(line)
            print("...")
            print(f"✅ Generated {len(code)} characters")
        else:
            print(f"❌ {lang}: Error - {response.status_code}")
            
    except Exception as e:
        print(f"❌ {lang}: Exception - {e}")

print("\n" + "=" * 50)
print("Multi-language testing complete!")
