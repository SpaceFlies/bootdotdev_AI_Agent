import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from config import MODEL_NAME
from call_function import available_functions

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
    model=MODEL_NAME,
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
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
    
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        
        
        print(f"Calling function: {function_call.name}({function_call.args})")
        
    else:
        print(f"Response: \n{response.text}")
    


if __name__ == "__main__":
    main()
