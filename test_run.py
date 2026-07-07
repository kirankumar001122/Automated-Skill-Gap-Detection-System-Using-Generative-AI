import requests
import json

# Test the run endpoint
url = "http://localhost:8000/api/v1/run-code"

# Test with factorial code
test_code = """def factorial(n):
    \"\"\"Calculate factorial of a number.\"\"\"
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Test the function
if __name__ == "__main__":
    for i in range(6):
        print(f"{i}! = {factorial(i)}")"""

data = {
    "code": test_code,
    "language": "python"
}

try:
    print("Testing run endpoint...")
    response = requests.post(url, json=data, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Code executed successfully!")
        
        # Check execution result
        if 'execution_result' in result:
            exec_result = result['execution_result']
            print(f"Execution Success: {exec_result.get('success', False)}")
            print(f"Execution Time: {exec_result.get('execution_time', 0):.3f}s")
            print(f"Output:\n{exec_result.get('output', 'No output')}")
        
        # Show agent tasks
        if 'agent_tasks' in result:
            print(f"\nAgent Tasks ({len(result['agent_tasks'])} agents):")
            for task in result['agent_tasks']:
                print(f"  - {task['agent_type']}: {task['status']} ({task.get('execution_time', 0):.2f}s)")
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
