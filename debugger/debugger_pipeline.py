from debugger.code_executor import execute_code
from debugger.error_parser import categorize_error
from debugger.gpt_integration import get_fix_suggestion

def debug_code_with_gpt(code: str) -> str:
    """
    Executes the code, identifies errors, and retrieves fix suggestions from GPT.

    Args:
        code (str): The Python code to debug.

    Returns:
        str: GPT's fix suggestion or explanation.
    """
    # Step 1: Execute the code and capture errors
    execution_output = execute_code(code)

    # Step 2: Categorize the error
    error_details = categorize_error(execution_output)

    # Step 3: If no error, return success message
    if error_details["type"] == "UnknownError":
        return "No errors detected. Your code executed successfully!"

    # Step 4: Get GPT fix suggestion
    gpt_suggestion = get_fix_suggestion(code, error_details)
    return gpt_suggestion

# Example usage
if __name__ == "__main__":
    code_to_debug = """
def test_function()
    print("Missing colon")
"""
    suggestion = debug_code_with_gpt(code_to_debug)
    print("GPT Fix Suggestion:\n", suggestion)
