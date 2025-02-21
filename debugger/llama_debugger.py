import logging
from llama_cpp import Llama

# Set up logging
logging.basicConfig(filename='debugger.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load Llama model (update the path to your downloaded model)
MODEL_PATH = "path/to/your/llama-2-7b.Q4_K_M.gguf"  # Update this to the correct model path

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
        # Ensure response has the expected structure
        if 'choices' in response and len(response['choices']) > 0:
            return response["choices"][0]["text"].strip()
        else:
            raise ValueError("Unexpected response structure from Llama.")
    except Exception as e:
        logging.error(f"Error while analyzing code with Llama: {e}")
        return "An error occurred while processing the code."
