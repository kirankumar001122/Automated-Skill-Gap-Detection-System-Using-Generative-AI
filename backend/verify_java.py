
import logging
import sys
import os
from services.local_executor import LocalExecutor

# Setup logging to see the detection process
logging.basicConfig(level=logging.INFO)

def test_java_examples():
    executor = LocalExecutor()
    
    examples = [
        {
            "name": "Hello World",
            "code": """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello from Java 21!");
    }
}
"""
        },
        {
            "name": "Odd/Even Checker",
            "code": """
public class Checker {
    public static void main(String[] args) {
        int num = 42;
        System.out.println(num + " is " + (num % 2 == 0 ? "even" : "odd"));
    }
}
"""
        },
        {
            "name": "Prime Number Generator",
            "code": """
public class PrimeGen {
    public static void main(String[] args) {
        System.out.print("Primes: ");
        for (int i = 2; i < 20; i++) {
            if (isPrime(i)) System.out.print(i + " ");
        }
    }
    static boolean isPrime(int n) {
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
}
"""
        },
        {
            "name": "Fibonacci",
            "code": """
public class Fib {
    public static void main(String[] args) {
        int n = 10, a = 0, b = 1;
        System.out.print("Fib: ");
        for (int i = 0; i < n; i++) {
            System.out.print(a + " ");
            int next = a + b;
            a = b;
            b = next;
        }
    }
}
"""
        }
    ]
    
    for ex in examples:
        print(f"\n--- Testing {ex['name']} ---")
        result = executor.execute_code(ex['code'], "java")
        print(f"Success: {result.success}")
        print(f"Output: {result.output.strip()}")
        if not result.success:
            print(f"Error: {result.error}")

if __name__ == "__main__":
    test_java_examples()
