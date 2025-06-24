import subprocess
import tempfile
import sys
import os


def execute_code(code: str, timeout: int = 10) -> str:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".py", encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        result = subprocess.run(
            [sys.executable, code],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "Code executed successfully (no output)"
        else:
            return result.stderr

    except subprocess.TimeoutExpired:
        return f"Error: Code execution timed out after {timeout} seconds."
    except Exception as e:
        return f"Execution error: {str(e)}"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
