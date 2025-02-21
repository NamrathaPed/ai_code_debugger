import re

def categorize_error(error_output: str) -> dict:
    """
    Parses the error output and categorizes the error type.
    """
    error_details = {
        "type": "UnknownError",
        "message": "No error detected.",
        "line_number": None,
        "raw_output": error_output.strip()
    }

    if "Error: Code execution timed out." in error_output:
        error_details["type"] = "TimeoutError"
        error_details["message"] = "The code execution timed out."
    elif "SyntaxError" in error_output:
        error_details["type"] = "SyntaxError"
        match = re.search(r"SyntaxError: (.+)", error_output)
        if match:
            error_details["message"] = match.group(1)
        line_match = re.search(r"File \".*\", line (\d+)", error_output)
        if line_match:
            error_details["line_number"] = int(line_match.group(1))
    elif "Traceback" in error_output:
        match = re.search(r"(?<=\n)(\w+Error): (.+)", error_output)
        if match:
            error_details["type"] = match.group(1)
            error_details["message"] = match.group(2)

        # Extract line number from traceback
        line_match = re.search(r"File \".*\", line (\d+)", error_output)
        if line_match:
            error_details["line_number"] = int(line_match.group(1))

    return error_details
