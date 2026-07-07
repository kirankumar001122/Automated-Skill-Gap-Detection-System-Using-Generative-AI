import requests
import json

# Test the backend API
url = "http://localhost:8000/api/v1/generate-code"
data = {
    "prompt": "Create a hello world function",
    "language": "python"
}

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
