import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from config import MODEL_NAME
from call_function import available_functions, call_function

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
    for _ in range(20):
        response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate)

        prompt_tokens = response.usage_metadata.prompt_token_count if response.usage_metadata != None else "N/A"
        response_tokens = response.usage_metadata.candidates_token_count if response.usage_metadata != None else "N/A"

        func_res_list = []
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")    
            print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
        
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not function_call_result.parts:
                raise Exception("Empty parts list from call_function")
            if not function_call_result.parts[0].function_response:
                raise Exception("Function response from call_function was None or not a FunctionResponse")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("The response from the function_response of call_function was None")
            func_res_list.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        
            messages.append(types.Content(role="user", parts=func_res_list))
        
        else:
            print(f"Response: \n{response.text}")
            break

        print("Iteration: ", _)
        if _ == 20:
            print("Reached maximum number of iterations. Exiting...")
            sys.exit(1)

        
            #print(f"Calling function: {function_call.name}({function_call.args})")
        
    
    


if __name__ == "__main__":
    main()
