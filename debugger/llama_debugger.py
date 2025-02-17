import logging
from llama_cpp import Llama

# Set up logging
logging.basicConfig(filename='debugger.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load Llama model (update the path to your downloaded model)
MODEL_PATH = "path/to/llama-2-7b.Q4_K_M.gguf"

try:
    llm = Llama(model_path=MODEL_PATH)
    logging.info("Llama model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load Llama model: {e}")
    raise

# Function to analyze code using Llama
def analyze_code_with_llama(code):
    try:
        prompt = f"Analyze the following Python code for bugs and suggest fixes:\n\n{code}\n\n"
        response = llm(prompt, max_tokens=200, stop=["\n"])
        return response["choices"][0]["text"].strip()
    except Exception as e:
        logging.error(f"Error while analyzing code with Llama: {e}")
        return "An error occurred while processing the code."

# Function to parse and debug a Python file
def run_debugger(file_path):
    try:
        with open(file_path, "r") as file:
            code = file.read()
        
        if not code.strip():
            raise ValueError("The file is empty.")
        
        print("Analyzing code with Llama...")
        result = analyze_code_with_llama(code)
        
        print("Debugging complete. Results:")
        print(result)
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the debugger
if __name__ == "__main__":
    file_to_debug = "some_code.py"
    run_debugger(file_to_debug)
