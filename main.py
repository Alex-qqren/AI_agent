import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import *
from call_function import available_functions, call_function
from config import *

import sys

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(MAX_ITERATIONS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print(f"Final response:\n{final_response}")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Exceeded maximum ({MAX_ITERATIONS}) numbers of iterations.")
    sys.exit(1)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Token counts are not available in the response.")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
    if not response.function_calls:
        print("Response:")
        print(response.text)
        return response.text
    
    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if len(function_call_result.parts) == 0:
            raise Exception("Function call result has no parts.")
        if function_call_result.parts[0].function_response is None:
            raise Exception("Function call result part has no function response.")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("Function call result part has no function response content.")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_results.append(function_call_result.parts[0])

    messages.append(types.Content(role="user", parts=function_results))

if __name__ == "__main__":
    main()
