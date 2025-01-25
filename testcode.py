from debugger.code_executor import execute_code

def test_execute_code():
    # Test 1: Successful code execution
    code1 = """
def test_function():
    print("Hello, world!")
    
test_function()
"""
    output1 = execute_code(code1)
    print("Test 1 - Successful Execution:\n", output1)

    # Test 2: Code with a runtime error
    code2 = """
def test_function():
    print("This will fail.")
    undefined_variable  # Runtime error
    
test_function()
"""
    output2 = execute_code(code2)
    print("Test 2 - Runtime Error:\n", output2)

    # Test 3: Code with a syntax error
    code3 = """
def test_function()
    print("Missing colon at the end of the function definition")
"""
    output3 = execute_code(code3)
    print("Test 3 - Syntax Error:\n", output3)

    # Test 4: Code that times out
    code4 = """
import time
time.sleep(15)  # This will exceed the timeout
"""
    output4 = execute_code(code4, timeout=5)  # Set timeout to 5 seconds
    print("Test 4 - Timeout:\n", output4)

    # Test 5: Empty code
    code5 = ""
    output5 = execute_code(code5)
    print("Test 5 - Empty Code:\n", output5)

# Run the tests
if __name__ == "__main__":
    test_execute_code()
