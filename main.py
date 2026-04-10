import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types


###Models and limits###
"""
gemini-2.5-flash
5 requests per minute
250k tokens per minute
20 requests per day


gemini-2.5-flash-lite
10 requests per minute
250k tokens per minute
20 requests per day

Gemini 3 Flash
gemini-3-flash-preview
5 requests per minute
250k tokens per minute
20 requests per day

Gemini 3.1 Flash Lite
gemini-3.1-flash-lite-preview
15 requests per minute
250k tokens per minute
500 requests per day
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Api key was not found. Did you set the correct variable name and pated the api key in the .env file?")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents= messages
    )
    
    if response.usage_metadata != None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    else:
        prompt_tokens = "N/A"
        response_tokens = "N/A"

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")    
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    
    print(f"Response: \n{response.text}")
    


if __name__ == "__main__":
    main()
