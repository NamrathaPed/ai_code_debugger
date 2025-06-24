from debugger.executor import execute_code
from debugger.parser import categorize_error
from ai_code_debugger.debugger.llama_debugger import analyze_code_with_llama

def debug_code_with_ai(code: str) -> str:
    """
    Executes the code, identifies errors, and retrieves suggestions from Llama.
    """
    # Step 1: Execute the code and capture errors
    execution_output = execute_code(code)

    # Step 2: Categorize the error
    error_details = categorize_error(execution_output)

    # Step 3: If no error, return success message
    if error_details["type"] == "UnknownError":
        return "No errors detected. Your code executed successfully!"

    # Step 4: Get AI fix suggestion
    ai_suggestion = analyze_code_with_llama(code)
    return ai_suggestion

# Example usage
if __name__ == "__main__":
    code_to_debug = """
def test_function()
    print("Missing colon")
"""
    suggestion = debug_code_with_ai(code_to_debug)
    print("AI Fix Suggestion:\n", suggestion)
