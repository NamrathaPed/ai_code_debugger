import subprocess
import sys
import os
import logging

def execute_code(code: str, timeout: int = 10) -> str:
    """
    Executes the provided code in a subprocess and captures errors or output.
    """
    # Create a temporary file to write the code to
    with open("temp_code.py", "w") as temp_file:
        temp_file.write(code)

    try:
        # Run the subprocess with the code file and capture stdout/stderr
        result = subprocess.run(
            [sys.executable, "temp_code.py"],  # Using the current Python interpreter
            capture_output=True,  # Capturing both stdout and stderr
            text=True,            # Capture as strings (not bytes)
            timeout=timeout      # Timeout for execution
        )

        # If the code executes successfully, return the stdout output
        if result.returncode == 0:
            return result.stdout
        else:
            # If there are errors, return stderr
            return result.stderr

    except subprocess.TimeoutExpired:
        logging.error("Code execution timed out.")
        return "Error: Code execution timed out."

    except Exception as e:
        logging.error(f"Execution failed: {e}")
        return f"Error: {str(e)}"

    finally:
        # Clean up the temporary code file after execution
        if os.path.exists("temp_code.py"):
            os.remove("temp_code.py")
