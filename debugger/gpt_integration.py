import os
from openai import OpenAI

# Initialize the OpenAI client with the API key
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("Client initialized successfully.")
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    exit(1)

# Test request to GPT
try:
    print("Sending request to GPT...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Updated to a model that is likely accessible
        messages=[{"role": "user", "content": "Hello, GPT. This is a test message."}],
    )
    print("Response received successfully:")
    print(response.choices[0].message.content)  # Print the response content
except Exception as e:
    print(f"An error occurred while communicating with GPT: {e}")

# Confirm the script has completed execution
print("Script completed successfully.")
