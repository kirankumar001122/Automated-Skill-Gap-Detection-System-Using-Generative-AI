#!/usr/bin/env python3
"""
Simple FastAPI server for demonstration
This is a minimal version that works without external dependencies
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import threading
import time
from datetime import datetime

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow requests from any origin
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.end_headers()
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/api/v1/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "Autonomous Coding Agent API",
                "status": "healthy",
                "service": "autonomous-coding-agent",
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/v1/models':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"models": ["codellama", "deepseek-coder", "llama3"]}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'] or 0)
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if self.path == '/api/v1/generate-code':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Mock response for demonstration
            response = {
                "task_id": f"task_{int(time.time())}",
                "status": "completed",
                "generated_code": self._generate_mock_code(data),
                "execution_result": {
                    "success": True,
                    "output": "Hello, World!\nCode executed successfully!",
                    "execution_time": 0.123
                },
                "explanation": "This is a simple demonstration of the Autonomous Coding Agent. The full version would include multi-agent processing with Ollama integration.",
                "agent_tasks": [
                    {
                        "agent_type": "planner",
                        "status": "completed",
                        "task_description": "Created execution plan",
                        "execution_time": 0.5
                    },
                    {
                        "agent_type": "code_generator",
                        "status": "completed", 
                        "task_description": "Generated code implementation",
                        "execution_time": 1.2
                    },
                    {
                        "agent_type": "debug",
                        "status": "completed",
                        "task_description": "Debugged and verified code",
                        "execution_time": 0.3
                    },
                    {
                        "agent_type": "test",
                        "status": "completed",
                        "task_description": "Generated and ran tests",
                        "execution_time": 0.8
                    },
                    {
                        "agent_type": "optimization",
                        "status": "completed",
                        "task_description": "Optimized code performance",
                        "execution_time": 0.4
                    },
                    {
                        "agent_type": "explanation",
                        "status": "completed",
                        "task_description": "Provided code explanation",
                        "execution_time": 0.6
                    }
                ],
                "created_at": datetime.now().isoformat(),
                "completed_at": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/v1/run-code':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Simulate code execution
            execution_result = self._simulate_code_execution(data.get("code", ""), data.get("language", "python"))
            
            response = {
                "task_id": f"task_{int(time.time())}",
                "status": "completed",
                "execution_result": execution_result,
                "agent_tasks": [
                    {
                        "agent_type": "planner",
                        "status": "completed",
                        "task_description": "Prepared execution environment",
                        "execution_time": 0.2
                    },
                    {
                        "agent_type": "code_generator",
                        "status": "completed", 
                        "task_description": "Validated code syntax",
                        "execution_time": 0.3
                    },
                    {
                        "agent_type": "debug",
                        "status": "completed",
                        "task_description": "Checked for runtime errors",
                        "execution_time": 0.4
                    },
                    {
                        "agent_type": "test",
                        "status": "completed",
                        "task_description": "Executed code and captured output",
                        "execution_time": 0.6
                    },
                    {
                        "agent_type": "optimization",
                        "status": "completed",
                        "task_description": "Optimized execution performance",
                        "execution_time": 0.2
                    },
                    {
                        "agent_type": "explanation",
                        "status": "completed",
                        "task_description": "Analyzed execution results",
                        "execution_time": 0.3
                    }
                ],
                "created_at": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/v1/debug-code':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Simulate debugging process
            debug_result = self._simulate_debug_process(data.get("code", ""), data.get("language", "python"))
            
            response = {
                "task_id": f"task_{int(time.time())}",
                "status": "completed",
                "generated_code": debug_result.get("fixed_code", data.get("code", "")),
                "execution_result": debug_result.get("execution_result"),
                "agent_tasks": [
                    {
                        "agent_type": "planner",
                        "status": "completed",
                        "task_description": "Analyzed code for potential issues",
                        "execution_time": 0.3
                    },
                    {
                        "agent_type": "debug",
                        "status": "completed",
                        "task_description": "Fixed identified bugs and issues",
                        "execution_time": 0.8
                    },
                    {
                        "agent_type": "test",
                        "status": "completed",
                        "task_description": "Verified fixes with test cases",
                        "execution_time": 0.5
                    },
                    {
                        "agent_type": "optimization",
                        "status": "completed",
                        "task_description": "Optimized fixed code",
                        "execution_time": 0.3
                    },
                    {
                        "agent_type": "explanation",
                        "status": "completed",
                        "task_description": "Documented debugging process",
                        "execution_time": 0.4
                    }
                ],
                "created_at": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/v1/optimize-code':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Simulate optimization process
            optimization_result = self._simulate_optimization_process(data.get("code", ""), data.get("language", "python"))
            
            response = {
                "task_id": f"task_{int(time.time())}",
                "status": "completed",
                "generated_code": optimization_result.get("optimized_code", data.get("code", "")),
                "optimization_suggestions": optimization_result.get("suggestions", []),
                "agent_tasks": [
                    {
                        "agent_type": "planner",
                        "status": "completed",
                        "task_description": "Identified optimization opportunities",
                        "execution_time": 0.4
                    },
                    {
                        "agent_type": "optimization",
                        "status": "completed",
                        "task_description": "Applied performance improvements",
                        "execution_time": 1.2
                    },
                    {
                        "agent_type": "test",
                        "status": "completed",
                        "task_description": "Validated optimized performance",
                        "execution_time": 0.6
                    },
                    {
                        "agent_type": "explanation",
                        "status": "completed",
                        "task_description": "Documented optimization changes",
                        "execution_time": 0.5
                    }
                ],
                "created_at": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/v1/explain-code':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Generate proper explanation
            explanation = self._generate_code_explanation(data.get("code", ""), data.get("language", "python"))
            
            response = {
                "task_id": f"task_{int(time.time())}",
                "status": "completed",
                "generated_code": data.get("code", "# Generated code"),
                "explanation": explanation,
                "agent_tasks": [
                    {
                        "agent_type": "planner",
                        "status": "completed",
                        "task_description": "Analyzed code structure",
                        "execution_time": 0.3
                    },
                    {
                        "agent_type": "explanation",
                        "status": "completed",
                        "task_description": "Generated detailed explanation",
                        "execution_time": 0.8
                    }
                ],
                "created_at": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def _generate_code_explanation(self, code, language):
        """Generate a detailed explanation of the code"""
        if not code.strip():
            return "No code provided for explanation."
        
        explanation = f"## Code Explanation ({language})\n\n"
        
        if "def factorial" in code:
            explanation += """This is a **factorial function** implementation in Python. Here's what it does:

### Purpose
The factorial function calculates the product of all positive integers up to a given number n. For example, 5! = 5 × 4 × 3 × 2 × 1 = 120.

### Key Components

1. **Input Validation**:
   - Checks if input is an integer using `isinstance(n, int)`
   - Raises `TypeError` for non-integer inputs
   - Raises `ValueError` for negative numbers

2. **Base Cases**:
   - Returns 1 for n = 0 or n = 1 (0! = 1! = 1)
   - These are mathematical definitions of factorial

3. **Recursive Calculation**:
   - Uses recursion: `n * factorial(n - 1)`
   - Each call reduces the problem size by 1
   - Eventually reaches the base case

4. **Test Section**:
   - Tests the function with values 0 through 5
   - Prints results in a formatted way

### Error Handling
- **Type Safety**: Ensures only integers are processed
- **Mathematical Validity**: Prevents negative number factorials
- **Clear Error Messages**: Descriptive error messages for debugging

### Time Complexity
- **Time**: O(n) - makes n recursive calls
- **Space**: O(n) - call stack depth of n

### Usage
```python
result = factorial(5)  # Returns 120
```

This implementation follows Python best practices and includes comprehensive error handling."""
        
        elif "def main()" in code or "if __name__ == \"__main__\"" in code:
            explanation += """This is a **Python main program** that demonstrates basic programming concepts:

### Structure
- **Function Definition**: Contains a `main()` function
- **Entry Point**: Uses `if __name__ == "__main__"` for script execution
- **Execution Flow**: Code runs when the script is executed directly

### Purpose
The program demonstrates:
- Function definition and calling
- String output with `print()`
- Basic arithmetic operations
- Program structure and organization

### Best Practices
- Uses main function for better code organization
- Follows Python naming conventions
- Includes docstrings for documentation"""
        
        else:
            explanation += f"""This is a **{language} code snippet** that demonstrates programming concepts:

### Code Analysis
- **Language**: {language}
- **Structure**: Well-formatted code with proper indentation
- **Purpose**: Implements specific functionality based on the code logic

### Key Features
- Clean, readable code structure
- Follows {language} best practices
- Includes proper error handling where applicable

### Usage
This code can be used as a reference or integrated into larger projects. Review the comments and structure to understand the implementation details."""
        
        return explanation
    
    def _simulate_debug_process(self, code, language):
        """Simulate debugging process"""
        return {
            "fixed_code": code,  # Return the code as-is (already working)
            "execution_result": {
                "success": True,
                "output": "Debugging complete. No issues found in the code.",
                "execution_time": 0.234
            }
        }
    
    def _simulate_optimization_process(self, code, language):
        """Simulate optimization process"""
        return {
            "optimized_code": code,  # Return the code as-is (already optimized)
            "suggestions": [
                "Code is already well-structured",
                "Consider adding type hints for better readability",
                "Performance is optimal for the current implementation"
            ]
        }
    
    def _simulate_code_execution(self, code, language):
        """Simulate code execution with realistic output"""
        if not code.strip():
            return {
                "success": False,
                "output": "",
                "error": "No code provided for execution",
                "execution_time": 0.0
            }
        
        # Simulate execution based on code content and language
        if "def factorial" in code or "factorial" in code:
            if language == "python":
                return {
                    "success": True,
                    "output": "0! = 1\n1! = 1\n2! = 2\n3! = 6\n4! = 24\n5! = 120\nFactorial function executed successfully!",
                    "execution_time": 0.156
                }
            elif language == "javascript":
                return {
                    "success": True,
                    "output": "0! = 1\n1! = 1\n2! = 2\n3! = 6\n4! = 24\n5! = 120\nFactorial function executed successfully!",
                    "execution_time": 0.089
                }
            elif language == "java":
                return {
                    "success": True,
                    "output": "0! = 1\n1! = 1\n2! = 2\n3! = 6\n4! = 24\n5! = 120\nFactorial function executed successfully!",
                    "execution_time": 0.234
                }
            elif language == "cpp":
                return {
                    "success": True,
                    "output": "0! = 1\n1! = 1\n2! = 2\n3! = 6\n4! = 24\n5! = 120\nFactorial function executed successfully!",
                    "execution_time": 0.178
                }
            elif language == "c":
                return {
                    "success": True,
                    "output": "0! = 1\n1! = 1\n2! = 2\n3! = 6\n4! = 24\n5! = 120\nFactorial function executed successfully!",
                    "execution_time": 0.145
                }
        elif "print(" in code or "console.log" in code or "System.out.println" in code or "std::cout" in code or "printf" in code:
            # Extract print statements and simulate output
            if language == "python":
                return {
                    "success": True,
                    "output": "Hello, World!\nCode executed successfully!",
                    "execution_time": 0.089
                }
            elif language == "javascript":
                return {
                    "success": True,
                    "output": "Hello, World!\nCode executed successfully!",
                    "execution_time": 0.067
                }
            elif language == "java":
                return {
                    "success": True,
                    "output": "Hello, World!\nCode executed successfully!",
                    "execution_time": 0.123
                }
            elif language == "cpp":
                return {
                    "success": True,
                    "output": "Hello, World!\nCode executed successfully!",
                    "execution_time": 0.098
                }
            elif language == "c":
                return {
                    "success": True,
                    "output": "Hello, World!\nCode executed successfully!",
                    "execution_time": 0.076
                }
        else:
            return {
                "success": True,
                "output": f"Code executed successfully!\nLanguage: {language}\nNo output generated (no print statements found).",
                "execution_time": 0.045
            }
    
    def _generate_mock_code(self, data):
        prompt = data.get("prompt", "").lower()
        language = data.get("language", "python")
        
        if "factorial" in prompt:
            if language == "python":
                return '''def factorial(n):
    """Calculate the factorial of a number."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Test the function
if __name__ == "__main__":
    for i in range(6):
        print(f"{i}! = {factorial(i)}")'''
            elif language == "javascript":
                return '''function factorial(n) {
    if (n < 0) {
        throw new Error("Factorial is not defined for negative numbers");
    }
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Test the function
for (let i = 0; i <= 5; i++) {
    console.log(`${i}! = ${factorial(i)}`);
}'''
            elif language == "java":
                return '''public class Factorial {
    public static long factorial(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Factorial is not defined for negative numbers");
        }
        if (n == 0 || n == 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    public static void main(String[] args) {
        for (int i = 0; i <= 5; i++) {
            System.out.println(i + "! = " + factorial(i));
        }
    }
}'''
            elif language == "cpp":
                return '''#include <iostream>
#include <stdexcept>

long factorial(int n) {
    if (n < 0) {
        throw std::invalid_argument("Factorial is not defined for negative numbers");
    }
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    for (int i = 0; i <= 5; i++) {
        std::cout << i << "! = " << factorial(i) << std::endl;
    }
    return 0;
}'''
            elif language == "c":
                return '''#include <stdio.h>
#include <stdlib.h>

long factorial(int n) {
    if (n < 0) {
        fprintf(stderr, "Factorial is not defined for negative numbers\\n");
        exit(1);
    }
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    for (int i = 0; i <= 5; i++) {
        printf("%d! = %ld\\n", i, factorial(i));
    }
    return 0;
}'''
        elif "fibonacci" in prompt:
            if language == "python":
                return '''def fibonacci(n):
    """Generate Fibonacci series up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    series = [0, 1]
    for i in range(2, n):
        series.append(series[-1] + series[-2])
    return series

# Test the function
if __name__ == "__main__":
    n = 10
    fib_series = fibonacci(n)
    print(f"Fibonacci series with {n} terms:")
    print(fib_series)
    for i, num in enumerate(fib_series):
        print(f"F({i}) = {num}")'''
            elif language == "javascript":
                return '''function fibonacci(n) {
    if (n <= 0) return [];
    if (n === 1) return [0];
    if (n === 2) return [0, 1];
    
    const series = [0, 1];
    for (let i = 2; i < n; i++) {
        series.push(series[i-1] + series[i-2]);
    }
    return series;
}

// Test the function
const n = 10;
const fibSeries = fibonacci(n);
console.log(`Fibonacci series with ${n} terms:`);
console.log(fibSeries);
fibSeries.forEach((num, i) => {
    console.log(`F(${i}) = ${num}`);
});'''
            elif language == "java":
                return '''public class Fibonacci {
    public static int[] fibonacci(int n) {
        if (n <= 0) return new int[0];
        if (n == 1) return new int[]{0};
        if (n == 2) return new int[]{0, 1};
        
        int[] series = new int[n];
        series[0] = 0;
        series[1] = 1;
        
        for (int i = 2; i < n; i++) {
            series[i] = series[i-1] + series[i-2];
        }
        return series;
    }
    
    public static void main(String[] args) {
        int n = 10;
        int[] fibSeries = fibonacci(n);
        System.out.println("Fibonacci series with " + n + " terms:");
        for (int i = 0; i < fibSeries.length; i++) {
            System.out.println("F(" + i + ") = " + fibSeries[i]);
        }
    }
}'''
            elif language == "cpp":
                return '''#include <iostream>
#include <vector>

std::vector<int> fibonacci(int n) {
    if (n <= 0) return {};
    if (n == 1) return {0};
    if (n == 2) return {0, 1};
    
    std::vector<int> series(n);
    series[0] = 0;
    series[1] = 1;
    
    for (int i = 2; i < n; i++) {
        series[i] = series[i-1] + series[i-2];
    }
    return series;
}

int main() {
    int n = 10;
    std::vector<int> fibSeries = fibonacci(n);
    std::cout << "Fibonacci series with " << n << " terms:" << std::endl;
    for (int i = 0; i < fibSeries.size(); i++) {
        std::cout << "F(" << i << ") = " << fibSeries[i] << std::endl;
    }
    return 0;
}'''
            elif language == "c":
                return '''#include <stdio.h>
#include <stdlib.h>

void fibonacci(int n, int* series) {
    if (n <= 0) return;
    if (n >= 1) series[0] = 0;
    if (n >= 2) series[1] = 1;
    
    for (int i = 2; i < n; i++) {
        series[i] = series[i-1] + series[i-2];
    }
}

int main() {
    int n = 10;
    int fibSeries[n];
    
    fibonacci(n, fibSeries);
    printf("Fibonacci series with %d terms:\\n", n);
    for (int i = 0; i < n; i++) {
        printf("F(%d) = %d\\n", i, fibSeries[i]);
    }
    return 0;
}'''
        elif "calculator" in prompt or "calculate" in prompt:
            if language == "python":
                return '''def calculator():
    """Simple calculator with basic operations."""
    print("Simple Calculator")
    print("Available operations: +, -, *, /")
    
    while True:
        try:
            num1 = float(input("Enter first number (or 'q' to quit): "))
            if num1 == 'q':
                break
                
            op = input("Enter operation (+, -, *, /): ")
            num2 = float(input("Enter second number: "))
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    print("Error: Division by zero!")
                    continue
                result = num1 / num2
            else:
                print("Invalid operation!")
                continue
                
            print(f"Result: {num1} {op} {num2} = {result}")
            print("-" * 30)
            
        except ValueError:
            print("Invalid input! Please enter numbers.")
        except KeyboardInterrupt:
            print("\\nGoodbye!")
            break

if __name__ == "__main__":
    calculator()'''
            elif language == "java":
                return '''import java.util.Scanner;

public class Calculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Simple Calculator");
        System.out.println("Available operations: +, -, *, /");
        
        while (true) {
            try {
                System.out.print("Enter first number (or 'q' to quit): ");
                String input = scanner.next();
                if (input.equalsIgnoreCase("q")) break;
                
                double num1 = Double.parseDouble(input);
                System.out.print("Enter operation (+, -, *, /): ");
                String op = scanner.next();
                System.out.print("Enter second number: ");
                double num2 = scanner.nextDouble();
                
                double result;
                switch (op) {
                    case "+":
                        result = num1 + num2;
                        break;
                    case "-":
                        result = num1 - num2;
                        break;
                    case "*":
                        result = num1 * num2;
                        break;
                    case "/":
                        if (num2 == 0) {
                            System.out.println("Error: Division by zero!");
                            continue;
                        }
                        result = num1 / num2;
                        break;
                    default:
                        System.out.println("Invalid operation!");
                        continue;
                }
                
                System.out.println("Result: " + num1 + " " + op + " " + num2 + " = " + result);
                System.out.println("------------------------------");
                
            } catch (NumberFormatException e) {
                System.out.println("Invalid input! Please enter numbers.");
            }
        }
        
        scanner.close();
        System.out.println("Goodbye!");
    }
}'''
            elif language == "javascript":
                return '''function calculator() {
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    console.log("Simple Calculator");
    console.log("Available operations: +, -, *, /");
    
    function askQuestion(query) {
        return new Promise(resolve => rl.question(query, resolve));
    }
    
    async function run() {
        while (true) {
            try {
                const input1 = await askQuestion("Enter first number (or 'q' to quit): ");
                if (input1.toLowerCase() === 'q') break;
                
                const num1 = parseFloat(input1);
                const op = await askQuestion("Enter operation (+, -, *, /): ");
                const input2 = await askQuestion("Enter second number: ");
                const num2 = parseFloat(input2);
                
                let result;
                switch (op) {
                    case '+':
                        result = num1 + num2;
                        break;
                    case '-':
                        result = num1 - num2;
                        break;
                    case '*':
                        result = num1 * num2;
                        break;
                    case '/':
                        if (num2 === 0) {
                            console.log("Error: Division by zero!");
                            continue;
                        }
                        result = num1 / num2;
                        break;
                    default:
                        console.log("Invalid operation!");
                        continue;
                }
                
                console.log(`Result: ${num1} ${op} ${num2} = ${result}`);
                console.log("------------------------------");
                
            } catch (error) {
                console.log("Invalid input! Please enter numbers.");
            }
        }
        
        console.log("Goodbye!");
        rl.close();
    }
    
    run();
}

calculator();'''
            elif language == "cpp":
                return '''#include <iostream>
#include <limits>
#include <cmath>

int main() {
    std::cout << "Simple Calculator" << std::endl;
    std::cout << "Available operations: +, -, *, /" << std::endl;
    
    while (true) {
        try {
            double num1, num2;
            char op;
            
            std::cout << "Enter first number (or 'q' to quit): ";
            std::string input;
            std::cin >> input;
            
            if (input == "q" || input == "Q") break;
            
            num1 = std::stod(input);
            
            std::cout << "Enter operation (+, -, *, /): ";
            std::cin >> op;
            
            std::cout << "Enter second number: ";
            std::cin >> num2;
            
            double result;
            switch (op) {
                case '+':
                    result = num1 + num2;
                    break;
                case '-':
                    result = num1 - num2;
                    break;
                case '*':
                    result = num1 * num2;
                    break;
                case '/':
                    if (num2 == 0) {
                        std::cout << "Error: Division by zero!" << std::endl;
                        continue;
                    }
                    result = num1 / num2;
                    break;
                default:
                    std::cout << "Invalid operation!" << std::endl;
                    continue;
            }
            
            std::cout << "Result: " << num1 << " " << op << " " << num2 << " = " << result << std::endl;
            std::cout << "------------------------------" << std::endl;
            
        } catch (const std::exception& e) {
            std::cout << "Invalid input! Please enter numbers." << std::endl;
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\\n');
        }
    }
    
    std::cout << "Goodbye!" << std::endl;
    return 0;
}'''
            elif language == "c":
                return '''#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main() {
    printf("Simple Calculator\\n");
    printf("Available operations: +, -, *, /\\n");
    
    while (1) {
        double num1, num2;
        char op;
        char input[100];
        
        printf("Enter first number (or 'q' to quit): ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;
        
        // Remove newline
        input[strcspn(input, "\\n")] = 0;
        
        if (input[0] == 'q' || input[0] == 'Q') break;
        
        num1 = atof(input);
        
        printf("Enter operation (+, -, *, /): ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;
        op = input[0];
        
        printf("Enter second number: ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;
        num2 = atof(input);
        
        double result;
        switch (op) {
            case '+':
                result = num1 + num2;
                break;
            case '-':
                result = num1 - num2;
                break;
            case '*':
                result = num1 * num2;
                break;
            case '/':
                if (num2 == 0) {
                    printf("Error: Division by zero!\\n");
                    continue;
                }
                result = num1 / num2;
                break;
            default:
                printf("Invalid operation!\\n");
                continue;
        }
        
        printf("Result: %.2f %c %.2f = %.2f\\n", num1, op, num2, result);
        printf("------------------------------\\n");
    }
    
    printf("Goodbye!\\n");
    return 0;
}'''
        elif "sorting" in prompt or "sort" in prompt:
            if language == "python":
                return '''def bubble_sort(arr):
    """Sort an array using bubble sort algorithm."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr):
    """Sort an array using quick sort algorithm."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Test the sorting functions
if __name__ == "__main__":
    import random
    
    # Generate random array
    array = [random.randint(1, 100) for _ in range(10)]
    print("Original array:", array)
    
    # Bubble sort
    bubble_sorted = bubble_sort(array.copy())
    print("Bubble sorted:", bubble_sorted)
    
    # Quick sort
    quick_sorted = quick_sort(array.copy())
    print("Quick sorted:", quick_sorted)'''
            elif language == "java":
                return '''import java.util.Arrays;
import java.util.Random;

public class SortingAlgorithms {
    
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
    
    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = (low - 1);
        
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        
        return i + 1;
    }
    
    public static void main(String[] args) {
        Random random = new Random();
        int[] array = new int[10];
        
        for (int i = 0; i < array.length; i++) {
            array[i] = random.nextInt(100) + 1;
        }
        
        System.out.println("Original array: " + Arrays.toString(array));
        
        int[] bubbleSorted = array.clone();
        bubbleSort(bubbleSorted);
        System.out.println("Bubble sorted: " + Arrays.toString(bubbleSorted));
        
        int[] quickSorted = array.clone();
        quickSort(quickSorted, 0, quickSorted.length - 1);
        System.out.println("Quick sorted: " + Arrays.toString(quickSorted));
    }
}'''
            elif language == "javascript":
                return '''function bubbleSort(arr) {
    // Sort an array using bubble sort algorithm
    const n = arr.length;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
        }
    }
    return arr;
}

function quickSort(arr) {
    // Sort an array using quick sort algorithm
    if (arr.length <= 1) return arr;
    
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);
    
    return [...quickSort(left), ...middle, ...quickSort(right)];
}

// Test the sorting functions
function main() {
    // Generate random array
    const array = Array.from({length: 10}, () => Math.floor(Math.random() * 100) + 1);
    console.log("Original array:", array);
    
    // Bubble sort
    const bubbleSorted = bubbleSort([...array]);
    console.log("Bubble sorted:", bubbleSorted);
    
    // Quick sort
    const quickSorted = quickSort([...array]);
    console.log("Quick sorted:", quickSorted);
}

main();'''
            elif language == "cpp":
                return '''#include <iostream>
#include <vector>
#include <algorithm>
#include <random>

void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    
    std::swap(arr[i + 1], arr[high]);
    return (i + 1);
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int main() {
    std::vector<int> array(10);
    
    // Generate random array
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 100);
    
    for (int i = 0; i < 10; i++) {
        array[i] = dis(gen);
    }
    
    std::cout << "Original array: ";
    for (int num : array) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    // Bubble sort
    std::vector<int> bubbleSorted = array;
    bubbleSort(bubbleSorted);
    std::cout << "Bubble sorted: ";
    for (int num : bubbleSorted) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    // Quick sort
    std::vector<int> quickSorted = array;
    quickSort(quickSorted, 0, quickSorted.size() - 1);
    std::cout << "Quick sorted: ";
    for (int num : quickSorted) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    return 0;
}'''
            elif language == "c":
                return '''#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    
    return (i + 1);
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");
}

int main() {
    int array[10];
    
    // Generate random array
    srand(time(NULL));
    for (int i = 0; i < 10; i++) {
        array[i] = rand() % 100 + 1;
    }
    
    printf("Original array: ");
    printArray(array, 10);
    
    // Bubble sort
    int bubbleSorted[10];
    for (int i = 0; i < 10; i++) {
        bubbleSorted[i] = array[i];
    }
    bubbleSort(bubbleSorted, 10);
    printf("Bubble sorted: ");
    printArray(bubbleSorted, 10);
    
    // Quick sort
    int quickSorted[10];
    for (int i = 0; i < 10; i++) {
        quickSorted[i] = array[i];
    }
    quickSort(quickSorted, 0, 9);
    printf("Quick sorted: ");
    printArray(quickSorted, 10);
    
    return 0;
}'''
        elif "prime" in prompt:
            if language == "python":
                return '''def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_primes(limit):
    """Generate all prime numbers up to a given limit."""
    primes = []
    for num in range(2, limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def main():
    print("Prime Number Checker")
    print("-" * 30)
    
    # Check specific numbers
    numbers_to_check = [2, 3, 4, 5, 16, 17, 19, 20, 23, 29]
    for num in numbers_to_check:
        if is_prime(num):
            print(f"{num} is prime")
        else:
            print(f"{num} is not prime")
    
    print("\\nPrimes up to 50:")
    primes = generate_primes(50)
    print(primes)
    print(f"Found {len(primes)} prime numbers")

if __name__ == "__main__":
    main()'''
            elif language == "java":
                return '''public class PrimeNumbers {
    
    public static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        
        for (int i = 3; i <= Math.sqrt(n); i += 2) {
            if (n % i == 0) return false;
        }
        return true;
    }
    
    public static void generatePrimes(int limit) {
        System.out.println("Prime numbers up to " + limit + ":");
        int count = 0;
        
        for (int num = 2; num <= limit; num++) {
            if (isPrime(num)) {
                System.out.print(num + " ");
                count++;
                if (count % 10 == 0) System.out.println();
            }
        }
        
        System.out.println("\\nFound " + count + " prime numbers");
    }
    
    public static void main(String[] args) {
        System.out.println("Prime Number Checker");
        System.out.println("------------------------------");
        
        int[] numbersToCheck = {2, 3, 4, 5, 16, 17, 19, 20, 23, 29};
        
        for (int num : numbersToCheck) {
            if (isPrime(num)) {
                System.out.println(num + " is prime");
            } else {
                System.out.println(num + " is not prime");
            }
        }
        
        System.out.println();
        generatePrimes(50);
    }
}'''
            elif language == "javascript":
                return '''function isPrime(n) {
    if (n <= 1) return false;
    if (n === 2) return true;
    if (n % 2 === 0) return false;
    
    for (let i = 3; i <= Math.sqrt(n); i += 2) {
        if (n % i === 0) return false;
    }
    return true;
}

function generatePrimes(limit) {
    const primes = [];
    for (let num = 2; num <= limit; num++) {
        if (isPrime(num)) {
            primes.push(num);
        }
    }
    return primes;
}

function main() {
    console.log("Prime Number Checker");
    console.log("------------------------------");
    
    const numbersToCheck = [2, 3, 4, 5, 16, 17, 19, 20, 23, 29];
    numbersToCheck.forEach(num => {
        if (isPrime(num)) {
            console.log(num + " is prime");
        } else {
            console.log(num + " is not prime");
        }
    });
    
    console.log("\\nPrimes up to 50:");
    const primes = generatePrimes(50);
    console.log(primes);
    console.log("Found " + primes.length + " prime numbers");
}

main();'''
            elif language == "cpp":
                return '''#include <iostream>
#include <vector>
#include <cmath>

bool isPrime(int n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (int i = 3; i <= std::sqrt(n); i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

std::vector<int> generatePrimes(int limit) {
    std::vector<int> primes;
    for (int num = 2; num <= limit; num++) {
        if (isPrime(num)) {
            primes.push_back(num);
        }
    }
    return primes;
}

int main() {
    std::cout << "Prime Number Checker" << std::endl;
    std::cout << "------------------------------" << std::endl;
    
    int numbersToCheck[] = {2, 3, 4, 5, 16, 17, 19, 20, 23, 29};
    int count = sizeof(numbersToCheck) / sizeof(numbersToCheck[0]);
    
    for (int i = 0; i < count; i++) {
        int num = numbersToCheck[i];
        if (isPrime(num)) {
            std::cout << num << " is prime" << std::endl;
        } else {
            std::cout << num << " is not prime" << std::endl;
        }
    }
    
    std::cout << "\\nPrimes up to 50:" << std::endl;
    std::vector<int> primes = generatePrimes(50);
    for (int prime : primes) {
        std::cout << prime << " ";
    }
    std::cout << "\\nFound " << primes.size() << " prime numbers" << std::endl;
    
    return 0;
}'''
            elif language == "c":
                return '''#include <stdio.h>
#include <stdbool.h>
#include <math.h>

bool isPrime(int n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (int i = 3; i <= sqrt(n); i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

void generatePrimes(int limit, int* primes, int* count) {
    *count = 0;
    for (int num = 2; num <= limit; num++) {
        if (isPrime(num)) {
            primes[*count] = num;
            (*count)++;
        }
    }
}

int main() {
    printf("Prime Number Checker\\n");
    printf("------------------------------\\n");
    
    int numbersToCheck[] = {2, 3, 4, 5, 16, 17, 19, 20, 23, 29};
    int count = sizeof(numbersToCheck) / sizeof(numbersToCheck[0]);
    
    for (int i = 0; i < count; i++) {
        int num = numbersToCheck[i];
        if (isPrime(num)) {
            printf("%d is prime\\n", num);
        } else {
            printf("%d is not prime\\n", num);
        }
    }
    
    printf("\\nPrimes up to 50:\\n");
    int primes[50];
    int primeCount;
    generatePrimes(50, primes, &primeCount);
    
    for (int i = 0; i < primeCount; i++) {
        printf("%d ", primes[i]);
    }
    printf("\\nFound %d prime numbers\\n", primeCount);
    
    return 0;
}'''
        elif "api" in prompt or "rest" in prompt:
            if language == "python":
                return '''from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    new_user['id'] = len(users) + 1
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)'''
        else:
            # Default code for all languages
            if language == "python":
                return '''# Autonomous Coding Agent Demo
def main():
    print("Hello from Autonomous Coding Agent!")
    print("This is a demonstration of the multi-agent system.")
    
    # Simple calculation
    result = sum(range(1, 11))
    print(f"Sum of numbers 1-10: {result}")

if __name__ == "__main__":
    main()'''
            elif language == "javascript":
                return '''// Autonomous Coding Agent Demo
function main() {
    console.log("Hello from Autonomous Coding Agent!");
    console.log("This is a demonstration of the multi-agent system.");
    
    // Simple calculation
    const result = Array.from({length: 10}, (_, i) => i + 1).reduce((a, b) => a + b, 0);
    console.log(`Sum of numbers 1-10: ${result}`);
}

main();'''
            elif language == "java":
                return '''public class AutonomousAgentDemo {
    public static void main(String[] args) {
        System.out.println("Hello from Autonomous Coding Agent!");
        System.out.println("This is a demonstration of the multi-agent system.");
        
        // Simple calculation
        int result = 0;
        for (int i = 1; i <= 10; i++) {
            result += i;
        }
        System.out.println("Sum of numbers 1-10: " + result);
    }
}'''
            elif language == "cpp":
                return '''#include <iostream>

int main() {
    std::cout << "Hello from Autonomous Coding Agent!" << std::endl;
    std::cout << "This is a demonstration of the multi-agent system." << std::endl;
    
    // Simple calculation
    int result = 0;
    for (int i = 1; i <= 10; i++) {
        result += i;
    }
    std::cout << "Sum of numbers 1-10: " << result << std::endl;
    
    return 0;
}'''
            elif language == "c":
                return '''#include <stdio.h>

int main() {
    printf("Hello from Autonomous Coding Agent!\\n");
    printf("This is a demonstration of the multi-agent system.\\n");
    
    // Simple calculation
    int result = 0;
    for (int i = 1; i <= 10; i++) {
        result += i;
    }
    printf("Sum of numbers 1-10: %d\\n", result);
    
    return 0;
}'''
            else:
                return f"# Generated {language} code for: {prompt}"

def run_server():
    """Run the simple HTTP server"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    
    print("🚀 Autonomous Coding Agent - Simple Server")
    print("=" * 50)
    print("📱 API Server running on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/v1/health")
    print("🔧 This is a demonstration version")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
