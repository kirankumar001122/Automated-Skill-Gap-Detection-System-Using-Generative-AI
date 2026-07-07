def factorial(n):
    """
    Calculate factorial of a number with proper error handling.
    
    Args:
        n (int): Non-negative integer
        
    Returns:
        int: Factorial of n
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    # Input validation
    if not isinstance(n, int):
        raise TypeError("Factorial function requires an integer input")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Base cases
    if n == 0 or n == 1:
        return 1
    
    # Recursive calculation
    return n * factorial(n - 1)


def test_factorial():
    """
    Comprehensive test suite for factorial function
    """
    print("Testing Factorial Function:")
    print("=" * 40)
    
    # Test cases: (input, expected_output)
    test_cases = [
        (0, 1),      # Edge case: zero
        (1, 1),      # Edge case: one
        (2, 2),      # Small number
        (3, 6),      # Small number
        (4, 24),     # Small number
        (5, 120),    # Medium number
        (10, 3628800) # Larger number
    ]
    
    # Run positive test cases
    print("Positive Test Cases:")
    for input_val, expected in test_cases:
        try:
            result = factorial(input_val)
            status = "✅ PASS" if result == expected else "❌ FAIL"
            print(f"  factorial({input_val}) = {result} (expected: {expected}) {status}")
        except Exception as e:
            print(f"  factorial({input_val}) raised {type(e).__name__}: {e} ❌ FAIL")
    
    # Test negative number case
    print("\nNegative Number Test:")
    try:
        factorial(-1)
        print("  factorial(-1) should raise ValueError ❌ FAIL")
    except ValueError as e:
        print(f"  factorial(-1) correctly raised ValueError: {e} ✅ PASS")
    except Exception as e:
        print(f"  factorial(-1) raised unexpected error: {e} ❌ FAIL")
    
    # Test non-integer input
    print("\nNon-integer Input Test:")
    try:
        factorial(3.5)
        print("  factorial(3.5) should raise TypeError ❌ FAIL")
    except TypeError as e:
        print(f"  factorial(3.5) correctly raised TypeError: {e} ✅ PASS")
    except Exception as e:
        print(f"  factorial(3.5) raised unexpected error: {e} ❌ FAIL")
    
    print("\n" + "=" * 40)
    print("All tests completed!")


if __name__ == "__main__":
    test_factorial()
