import subprocess
import tempfile
import sys
import os

def execute_code(code: str, timeout: int = 10) -> str:
    """
    Execute Python code in a temporary file and return the output.
    
    Args:
        code (str): Python code to execute
        timeout (int): Maximum execution time in seconds
    
    Returns:
        str: Output from code execution or error message
    """
    tmp_path = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".py", encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        
        # Execute the code
        result = subprocess.run(
            [sys.executable, tmp_path], 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            encoding='utf-8'
        )
        
        # Return output or error
        if result.returncode == 0:
            return result.stdout if result.stdout else "Code executed successfully (no output)"
        else:
            return result.stderr
            
    except subprocess.TimeoutExpired:
        return f"Error: Code execution timed out after {timeout} seconds."
    except Exception as e:
        return f"Execution error: {str(e)}"
    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass  # File cleanup failed, but continue