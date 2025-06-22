#!/usr/bin/env python3
"""
AI Code Debugger - Main Application
A Python debugging tool that uses AI analysis to help fix code errors.
"""

import sys
import os
import argparse
from typing import Optional

# Import our modules
from executor import execute_code
from parser import categorize_error, get_error_suggestions
from llama_debugger import analyze_code_with_llama, debugger

def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("🐍 AI PYTHON CODE DEBUGGER")
    print("=" * 60)
    print("An intelligent debugging assistant powered by AI")
    print("-" * 60)

def print_error_details(error_info: dict):
    """Print formatted error information."""
    print("\n📊 ERROR ANALYSIS:")
    print("-" * 30)
    print(f"Type: {error_info['type']}")
    print(f"Severity: {error_info['severity'].upper()}")
    if error_info['line_number']:
        print(f"Line: {error_info['line_number']}")
    print(f"Message: {error_info['message']}")

def print_suggestions(suggestions: list):
    """Print basic suggestions."""
    if suggestions:
        print("\n💡 QUICK SUGGESTIONS:")
        print("-" * 30)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")

def print_ai_analysis(analysis: str):
    """Print AI analysis results."""
    print("\n🤖 AI ANALYSIS:")
    print("-" * 30)
    print(analysis)

def debug_code_from_string(code: str, timeout: int = 10, model_path: Optional[str] = None) -> dict:
    """
    Debug Python code from string input.
    
    Args:
        code (str): Python code to debug
        timeout (int): Execution timeout in seconds
        model_path (str, optional): Path to LLaMA model
    
    Returns:
        dict: Debug results
    """
    # Initialize model if path provided
    if model_path and not debugger.model_loaded:
        debugger.load_model(model_path)
    
    print("🔄 Executing code...")
    
    # Execute the code
    output = execute_code(code, timeout)
    
    # Categorize any errors
    error_info = categorize_error(output)
    
    # Get basic suggestions
    suggestions = get_error_suggestions(error_info)
    
    # Get AI analysis
    ai_analysis = analyze_code_with_llama(code, error_info)
    
    results = {
        'code': code,
        'output': output,
        'error_info': error_info,
        'suggestions': suggestions,
        'ai_analysis': ai_analysis,
        'success': error_info['type'] == 'NoError'
    }
    
    return results

def debug_code_from_file(file_path: str, timeout: int = 10, model_path: Optional[str] = None) -> dict:
    """
    Debug Python code from file.
    
    Args:
        file_path (str): Path to Python file
        timeout (int): Execution timeout
        model_path (str, optional): Path to LLaMA model
    
    Returns:
        dict: Debug results
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return debug_code_from_string(code, timeout, model_path)
    except FileNotFoundError:
        return {
            'error': f"File not found: {file_path}",
            'success': False
        }
    except Exception as e:
        return {
            'error': f"Error reading file: {str(e)}",
            'success': False
        }

def interactive_mode(model_path: Optional[str] = None):
    """Run in interactive mode."""
    print_banner()
    print("Interactive Mode - Enter your Python code (type 'EXIT' to quit)")
    print("Type 'MULTILINE' for multi-line code input")
    print("Type 'HELP' for available commands")
    
    if model_path:
        print(f"LLaMA Model: {model_path}")
    else:
        print("LLaMA Model: Not configured (using fallback analysis)")
    
    print("\n" + "=" * 60)
    
    while True:
        try:
            print("\n➤ Enter command or Python code:")
            user_input = input("> ").strip()
            
            if user_input.upper() == 'EXIT':
                print("👋 Goodbye!")
                break
            elif user_input.upper() == 'HELP':
                print("""
Available commands:
- EXIT: Quit the debugger
- MULTILINE: Enter multi-line code
- HELP: Show this help message
- Any Python code: Debug the code
                """)
                continue
            elif user_input.upper() == 'MULTILINE':
                print("Enter multi-line code (type 'END' on a new line to finish):")
                code_lines = []
                while True:
                    line = input("  ")
                    if line.strip().upper() == 'END':
                        break
                    code_lines.append(line)
                user_input = '\n'.join(code_lines)
            
            if user_input.strip():
                results = debug_code_from_string(user_input, model_path=model_path)
                
                # Display results
                if results['success']:
                    print("\n✅ CODE EXECUTED SUCCESSFULLY!")
                    if results['output']:
                        print(f"Output: {results['output']}")
                else:
                    print("\n❌ ERROR DETECTED!")
                    print_error_details(results['error_info'])
                    print_suggestions(results['suggestions'])
                    print_ai_analysis(results['ai_analysis'])
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="AI Python Code Debugger",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Interactive mode
  python main.py -f script.py             # Debug file
  python main.py -c "print('hello')"      # Debug code string
  python main.py -m /path/to/model.gguf   # Use LLaMA model
        """
    )
    
    parser.add_argument('-f', '--file', 
                       help='Python file to debug')
    parser.add_argument('-c', '--code', 
                       help='Python code string to debug')
    parser.add_argument('-m', '--model', 
                       help='Path to LLaMA model file (.gguf)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                       help='Code execution timeout in seconds (default: 10)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress banner and extra output')
    
    args = parser.parse_args()
    
    # Validate model path if provided
    if args.model and not os.path.exists(args.model):
        print(f"❌ Error: Model file not found: {args.model}")
        sys.exit(1)
    
    # Handle file debugging
    if args.file:
        if not args.quiet:
            print_banner()
            print(f"🔍 Debugging file: {args.file}")
        
        results = debug_code_from_file(args.file, args.timeout, args.model)
        
        if 'error' in results:
            print(f"❌ {results['error']}")
            sys.exit(1)
        
        # Display results
        if results['success']:
            print("✅ CODE EXECUTED SUCCESSFULLY!")
            if results['output']:
                print(f"Output:\n{results['output']}")
        else:
            print("❌ ERROR DETECTED!")
            print_error_details(results['error_info'])
            print_suggestions(results['suggestions'])
            print_ai_analysis(results['ai_analysis'])
    
    # Handle code string debugging
    elif args.code:
        if not args.quiet:
            print_banner()
            print("🔍 Debugging code string...")
        
        results = debug_code_from_string(args.code, args.timeout, args.model)
        
        # Display results
        if results['success']:
            print("✅ CODE EXECUTED SUCCESSFULLY!")
            if results['output']:
                print(f"Output:\n{results['output']}")
        else:
            print("❌ ERROR DETECTED!")
            print_error_details(results['error_info'])
            print_suggestions(results['suggestions'])
            print_ai_analysis(results['ai_analysis'])
    
    # Default to interactive mode
    else:
        interactive_mode(args.model)

if __name__ == "__main__":
    main()