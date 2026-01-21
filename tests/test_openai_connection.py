import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_connection():
    print("--- Testing OpenAI API Connection ---")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("FAILURE: OPENAI_API_KEY not found in environment variables.")
        return

    print(f"API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, are you working?"}
            ],
            max_tokens=10
        )
        content = response.choices[0].message.content
        print(f"\nResponse from OpenAI: {content}")
        print("\nSUCCESS: OpenAI API connection established.")
        
    except Exception as e:
        print(f"\nFAILURE: OpenAI API connection failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_openai_connection()
