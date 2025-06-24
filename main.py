import sys
import os
import argparse
from typing import Optional, List, Dict, Any

# Import our modules from the debugger package
from debugger.executor import execute_code
from debugger.parser import categorize_error, get_error_suggestions
from debugger.gemini_debugger import analyze_code_with_gemini

def print_banner() -> None:
    """Print the application banner with Unicode decorations."""
    print("=" * 60)
    print("\U0001F40D AI PYTHON CODE DEBUGGER (Gemini Edition)")
    print("=" * 60)
    print("An intelligent debugging assistant powered by Gemini AI")
    print("-" * 60)

def print_error_details(error_info: Dict[str, Any]) -> None:
    """
    Print formatted error information.
    
    Args:
        error_info: Dictionary containing error details
    """
    print("\n\U0001F4CA ERROR ANALYSIS:")
    print("-" * 30)
    print(f"Type: {error_info['type']}")
    print(f"Severity: {error_info['severity'].upper()}")
    if error_info.get('line_number'):
        print(f"Line: {error_info['line_number']}")
    print(f"Message: {error_info['message']}")

def main() -> None:
    """Main execution function"""
    print_banner()
    
    parser = argparse.ArgumentParser(description='AI Python Code Debugger')
    parser.add_argument('file', help='Python file to debug')
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    # Read the code from the file
    try:
        with open(args.file, 'r') as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    print(f"\n\U0001F50D ANALYZING: {args.file}")
    print("-" * 40)
    
    # Execute the code and capture any errors
    execution_result = execute_code(args.file)
    
    # Check if there's an error (handle both string and object returns)
    if hasattr(execution_result, 'error') and execution_result.error:
        # If execute_code returns an object with error attribute
        error_info = categorize_error(execution_result.error)
        print_error_details(error_info)
        
        # Get AI analysis from Gemini
        print("\n\U0001F916 GEMINI AI ANALYSIS:")
        print("-" * 40)
        try:
            ai_analysis = analyze_code_with_gemini(code_content, error_info)
            print(ai_analysis)
        except Exception as e:
            print(f"AI analysis failed: {e}")
            # Fallback to basic suggestions
            suggestions = get_error_suggestions(error_info)
            if suggestions:
                print("\n\U0001F4A1 BASIC SUGGESTIONS:")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion}")
    
    elif isinstance(execution_result, str) and execution_result.strip():
        # If execute_code returns a string with error content
        if "Error" in execution_result or "Traceback" in execution_result:
            # Parse the error from the string
            error_info = categorize_error(execution_result)
            print_error_details(error_info)
            
            # Get AI analysis from Gemini
            print("\n\U0001F916 GEMINI AI ANALYSIS:")
            print("-" * 40)
            try:
                ai_analysis = analyze_code_with_gemini(code_content, error_info)
                print(ai_analysis)
            except Exception as e:
                print(f"AI analysis failed: {e}")
                # Fallback to basic suggestions
                suggestions = get_error_suggestions(error_info)
                if suggestions:
                    print("\n\U0001F4A1 BASIC SUGGESTIONS:")
                    for i, suggestion in enumerate(suggestions, 1):
                        print(f"{i}. {suggestion}")
        else:
            print("\n\U0001F389 SUCCESS: Code executed without errors!")
            print(f"Output:\n{execution_result}")
    else:
        print("\n\U0001F389 SUCCESS: Code executed without errors!")

if __name__ == '__main__':
    main()