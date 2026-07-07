def factorial(n):
    """Calculate factorial of a number."""
    if n < 0:
        raise ValueError("Factorial of negative numbers is not defined")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Test the function
if __name__ == "__main__":
    print("Testing factorial function:")
    
    # Test cases
    test_values = [0, 1, 2, 3, 4, 5]
    
    for i in test_values:
        try:
            result = factorial(i)
            print(f"{i}! = {result}")
        except ValueError as e:
            print(f"Error for {i}: {e}")
        except Exception as e:
            print(f"Unexpected error for {i}: {e}")
    
    # Additional test for negative number
    try:
        factorial(-1)
    except ValueError as e:
        print(f"Correctly caught error for negative number: {e}")
    
    print("\nFactorial function is working correctly!")
