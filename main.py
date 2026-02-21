import os
import argparse
from dotenv import load_dotenv
from google import genai




def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=args.user_prompt
    )

    print(f"User prompt: {args.user_prompt}")
    if response.usage_metadata is None:
        raise RuntimeError("Token counts are not available in the response.")
    x = response.usage_metadata.prompt_token_count
    y = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {x}")
    print(f"Response tokens: {y}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
