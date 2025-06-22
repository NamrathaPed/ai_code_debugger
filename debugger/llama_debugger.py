import logging
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    filename="debugger.log", 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LlamaDebugger:
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the LLaMA debugger.
        
        Args:
            model_path (str, optional): Path to LLaMA model file
        """
        self.llm = None
        self.model_loaded = False
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            logging.warning("LLaMA model not found or path not provided. Using fallback analysis.")
    
    def load_model(self, model_path: str) -> bool:
        """
        Load the LLaMA model.
        
        Args:
            model_path (str): Path to the model file
            
        Returns:
            bool: True if model loaded successfully
        """
        try:
            from llama_cpp import Llama
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,  # Context window
                n_threads=4,  # Number of threads
                verbose=False
            )
            self.model_loaded = True
            logging.info(f"LLaMA model loaded successfully from {model_path}")
            return True
        except ImportError:
            logging.error("llama-cpp-python not installed. Install with: pip install llama-cpp-python")
            return False
        except Exception as e:
            logging.error(f"Failed to load LLaMA model: {e}")
            return False
    
    def analyze_code_with_llama(self, code: str, error_details: dict) -> str:
        """
        Analyze code using LLaMA AI model.
        
        Args:
            code (str): The Python code to analyze
            error_details (dict): Error information from parser
            
        Returns:
            str: AI analysis and suggestions
        """
        if not self.model_loaded:
            return self._fallback_analysis(code, error_details)
        
        # Create detailed prompt
        prompt = self._create_analysis_prompt(code, error_details)
        
        try:
            response = self.llm(
                prompt,
                max_tokens=800,
                temperature=0.1,  # Low temperature for consistent responses
                top_p=0.9,
                stop=["```", "---"]
            )
            
            analysis = response["choices"][0]["text"].strip()
            logging.info("LLaMA analysis completed successfully")
            return analysis
            
        except Exception as e:
            logging.error(f"LLaMA analysis failed: {e}")
            return self._fallback_analysis(code, error_details)
    
    def _create_analysis_prompt(self, code: str, error_details: dict) -> str:
        """Create a structured prompt for LLaMA analysis."""
        prompt = f"""You are an expert Python debugger. Analyze this code and provide help.

CODE TO DEBUG:
```python
{code}
```

ERROR INFORMATION:
- Type: {error_details.get('type', 'Unknown')}
- Message: {error_details.get('message', 'No message')}
- Line: {error_details.get('line_number', 'Unknown')}
- Severity: {error_details.get('severity', 'medium')}

Please provide:
1. ERROR EXPLANATION: What caused this error?
2. SOLUTION: How to fix it step by step
3. CORRECTED CODE: The fixed version of the code
4. PREVENTION: How to avoid this error in the future

Keep your response concise and practical."""
        
        return prompt
    
    def _fallback_analysis(self, code: str, error_details: dict) -> str:
        """
        Provide basic analysis when LLaMA is not available.
        
        Args:
            code (str): The Python code
            error_details (dict): Error information
            
        Returns:
            str: Basic analysis
        """
        error_type = error_details.get('type', 'Unknown')
        error_message = error_details.get('message', 'No message available')
        line_number = error_details.get('line_number')
        
        analysis = f"""BASIC ANALYSIS (LLaMA not available):

ERROR TYPE: {error_type}
ERROR MESSAGE: {error_message}
"""
        
        if line_number:
            analysis += f"LINE NUMBER: {line_number}\n"
        
        # Add basic suggestions based on error type
        if error_type == "SyntaxError":
            analysis += """
COMMON CAUSES:
- Missing colons (:) after if/for/while/def statements
- Unmatched parentheses, brackets, or quotes
- Incorrect indentation
- Typos in Python keywords

SOLUTION STEPS:
1. Check line {line_number} for syntax issues
2. Verify all parentheses and brackets are properly closed
3. Ensure consistent indentation (use spaces or tabs, not both)
4. Check for typos in keywords like 'if', 'for', 'def', etc.
""".format(line_number=line_number or "mentioned in error")
        
        elif error_type == "NameError":
            analysis += """
COMMON CAUSES:
- Using a variable before defining it
- Typos in variable names
- Variable out of scope

SOLUTION STEPS:
1. Define the variable before using it
2. Check spelling of variable names
3. Ensure variable is accessible in current scope
"""
        
        elif error_type == "ImportError":
            analysis += """
COMMON CAUSES:
- Required module not installed
- Incorrect module name
- Module not in Python path

SOLUTION STEPS:
1. Install missing module: pip install <module_name>
2. Check module name spelling
3. Verify module compatibility with Python version
"""
        
        analysis += "\nFor detailed AI analysis, install and configure LLaMA model."
        return analysis

# Global instance
debugger = LlamaDebugger()

def analyze_code_with_llama(code: str, error_details: dict) -> str:
    """
    Convenience function for backward compatibility.
    """
    return debugger.analyze_code_with_llama(code, error_details)