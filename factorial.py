def factorial(n):
    # Intentional bug: the base case for recursion is not correctly defined
    if n == 0:
        return 0
    else:
        return n * factorial(n - 1)

# Test the function
try:
    number = 5
    result = factorial(number)
    print(f"The factorial of {number} is {result}")
except RecursionError:
    print("Error: This function caused a recursion error.")