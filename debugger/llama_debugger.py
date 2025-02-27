import logging
from llama_cpp import Llama

logging.basicConfig(
    filename='debugger.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MODEL_PATH = "path/to/llama-2-7b.Q4_K_M.gguf"

try:
    llm = Llama(model_path=MODEL_PATH)
    logging.info("Llama model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load Llama model: {e}")
    raise

def analyze_code_with_llama(code, error_details=None):
    try:
        prompt = f"""
        You are an advanced AI code debugger. Analyze the following Python code and provide:
        - A clear explanation of any errors found.
        - Suggested fixes with corrected code examples.
        - If no errors exist, provide possible optimizations.
        
        Code:
        {code}
        
        """
        if error_details:
            prompt += f"\nError details: {error_details}\n"

        response = llm(prompt, max_tokens=500, stop=["\n"])
        
        return response["choices"][0]["text"].strip()
    except Exception as e:
        logging.error(f"Error while analyzing code with Llama: {e}")
        return "An error occurred while processing the code."
