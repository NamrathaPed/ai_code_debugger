import os
import openai

# Load the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_fix_suggestion(code: str, error_details: dict, model: str = "gpt-4") -> str:
    """
    Fetches a fix suggestion from GPT for the given code and error details.
    """
    if not openai.api_key:
        return "Error: OpenAI API key is not set. Please configure it in your environment variables."

    # Prepare the prompt
    prompt = f"""
    The following Python code contains an error:

    {code}

    Error Details:
    - Error Type: {error_details.get('type')}
    - Message: {error_details.get('message')}
    - Line Number: {error_details.get('line_number')}

    Please suggest a fix for this error and explain why the fix works.
    """

    try:
        # Send the prompt to GPT (updated for new API)
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=100,  # Adjust token limit as needed
            n=1,
            stop=None,
            temperature=0.5
        )

        # Extract GPT's response
        suggestion = response.choices[0].text.strip()
        return suggestion

    except Exception as e:
        return f"Error communicating with GPT: {str(e)}"

# Call the function and print the result
if __name__ == "__main__":
    code_to_debug = """
def test_function()
    print("Missing colon")
"""
    error_details = {
        "type": "SyntaxError",
        "message": "invalid syntax",
        "line_number": 2
    }

    suggestion = get_fix_suggestion(code_to_debug, error_details)
    print("GPT Fix Suggestion:\n", suggestion)

