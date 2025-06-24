import logging
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    filename="debugger.log", 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GeminiDebugger:
    def __init__(self, model_name: str = "gemini-pro"):
        """
        Initialize the Gemini debugger.
        """
        self.model_name = model_name
        
        # Try to import and configure Gemini
        try:
            import google.generativeai as genai
            from google.generativeai import GenerativeModel
            
            # Configure API key from environment variable
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.model_loaded = True
                self.model = GenerativeModel(model_name)
                logging.info(f"Gemini model '{model_name}' initialized with API key.")
            else:
                self.model_loaded = False
                self.model = None
                logging.warning("Gemini API key not found. Using fallback mode.")
                print("⚠️  Gemini API key not configured. Set GEMINI_API_KEY environment variable for AI analysis.")
        except ImportError:
            self.model_loaded = False
            self.model = None
            logging.error("Google Generative AI package not installed. Using fallback mode.")
            print("⚠️  Google Generative AI package not found. Install with: pip install google-generativeai")
        except Exception as e:
            self.model_loaded = False
            self.model = None
            logging.error(f"Failed to initialize Gemini: {e}")
            print(f"⚠️  Failed to initialize Gemini: {e}")

    def analyze_code_with_gemini(self, code: str, error_details: dict) -> str:
        """
        Analyze code using Gemini AI model.

        Args:
            code (str): The Python code to analyze
            error_details (dict): Error information from parser

        Returns:
            str: AI analysis and suggestions
        """
        if not self.model_loaded:
            return self._fallback_analysis(code, error_details)

        prompt = self._create_analysis_prompt(code, error_details)

        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logging.info("Gemini analysis completed successfully")
            return result
        except Exception as e:
            logging.error(f"Gemini analysis failed: {e}")
            return self._fallback_analysis(code, error_details)

    def _create_analysis_prompt(self, code: str, error_details: dict) -> str:
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
        error_type = error_details.get('type', 'Unknown')
        error_message = error_details.get('message', 'No message available')
        line_number = error_details.get('line_number')

        analysis = f"""BASIC ANALYSIS (Gemini not available):

ERROR TYPE: {error_type}
ERROR MESSAGE: {error_message}
"""
        if line_number:
            analysis += f"LINE NUMBER: {line_number}\n"

        if error_type == "SyntaxError":
            analysis += """
COMMON CAUSES:
- Missing colons (:) after if/for/while/def statements
- Unmatched parentheses, brackets, or quotes
- Incorrect indentation
- Typos in Python keywords

SOLUTION STEPS:
1. Check line for syntax issues
2. Verify all parentheses and brackets are properly closed
3. Ensure consistent indentation (use spaces or tabs, not both)
4. Check for typos in keywords like 'if', 'for', 'def', etc.
"""
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
        analysis += "\nFor detailed AI analysis, configure Gemini API properly."
        return analysis

# Global instance
debugger = GeminiDebugger()

def analyze_code_with_gemini(code: str, error_details: dict) -> str:
    """Global function to analyze code with Gemini"""
    return debugger.analyze_code_with_gemini(code, error_details)