import re

def categorize_error(error_output: str) -> dict:
    error_output = error_output.strip()

    if not error_output or "Code executed successfully" in error_output:
        return {
            "type": "NoError",
            "message": "",
            "line_number": None,
            "raw_output": error_output,
            "severity": "none"
        }

    error = {
        "type": "UnknownError",
        "message": error_output,
        "line_number": None,
        "raw_output": error_output,
        "severity": "medium"
    }

    if "timed out" in error_output.lower():
        error.update({
            "type": "TimeoutError",
            "message": "Code execution exceeded time limit",
            "severity": "high"
        })
        return error

    if "SyntaxError" in error_output:
        error["type"] = "SyntaxError"
        error["severity"] = "high"

        syntax_match = re.search(r"SyntaxError: (.+)", error_output)
        if syntax_match:
            error["message"] = syntax_match.group(1).strip()

        line_match = re.search(r"line (\d+)", error_output)
        if line_match:
            error["line_number"] = int(line_match.group(1))

    elif "Traceback" in error_output:
        error_match = re.search(r"(\w+Error): (.+)", error_output)
        if error_match:
            error["type"] = error_match.group(1)
            error["message"] = error_match.group(2).strip()

        line_match = re.search(r"line (\d+)", error_output)
        if line_match:
            error["line_number"] = int(line_match.group(1))

        critical_errors = ["SystemExit", "KeyboardInterrupt", "MemoryError"]
        if error["type"] in critical_errors:
            error["severity"] = "critical"
        elif error["type"] in ["NameError", "TypeError", "AttributeError"]:
            error["severity"] = "high"
        else:
            error["severity"] = "medium"

    elif "ModuleNotFoundError" in error_output or "ImportError" in error_output:
        error["type"] = "ImportError"
        error["severity"] = "high"
        import_match = re.search(r"No module named '(.+)'", error_output)
        if import_match:
            error["message"] = f"Missing module: {import_match.group(1)}"

    return error


def get_error_suggestions(error_info: dict) -> list:
    suggestions = []
    error_type = error_info.get("type", "")

    if error_type == "SyntaxError":
        suggestions = [
            "Check for missing colons, parentheses, or brackets",
            "Verify proper indentation",
            "Look for typos in keywords"
        ]
    elif error_type == "NameError":
        suggestions = [
            "Check if variable is defined before use",
            "Verify correct spelling of variable names",
            "Make sure variables are in the correct scope"
        ]
    elif error_type == "ImportError":
        suggestions = [
            "Install the required module using pip",
            "Check if the module name is spelled correctly",
            "Verify the module is available in your environment"
        ]
    elif error_type == "TypeError":
        suggestions = [
            "Check data types being used in operations",
            "Verify function arguments match expected types",
            "Look for unsupported operations between types"
        ]
    elif error_type == "TimeoutError":
        suggestions = [
            "Check for infinite loops",
            "Optimize code performance",
            "Consider breaking down complex operations"
        ]
    else:
        suggestions = [
            "Read the error message carefully",
            "Check the line number mentioned in the error",
            "Review the code logic around the error location"
        ]

    return suggestions
