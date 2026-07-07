import requests
import json

# Test the explanation endpoint
url = "http://localhost:8000/api/v1/explain-code"

# Test with factorial code
test_code = """
def factorial(n):
    \"\"\"Calculate factorial of a number with proper error handling.\"\"\"
    if not isinstance(n, int):
        raise TypeError("Factorial function requires an integer input")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    return n * factorial(n - 1)

# Test the function
if __name__ == "__main__":
    for i in range(6):
        print(f"{i}! = {factorial(i)}")
"""

data = {
    "code": test_code,
    "language": "python"
}

try:
    print("Testing explanation endpoint...")
    response = requests.post(url, json=data, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Explanation generated successfully!")
        print("\nGenerated Explanation:")
        print("=" * 50)
        print(result.get('explanation', 'No explanation provided'))
        print("=" * 50)
        
        # Show agent tasks
        if 'agent_tasks' in result:
            print("\nAgent Tasks:")
            for task in result['agent_tasks']:
                print(f"  - {task['agent_type']}: {task['status']} ({task.get('execution_time', 0):.2f}s)")
    else:
        print(f"❌ Error: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ Timeout: Request took too long")
except Exception as e:
    print(f"❌ Error: {e}")
