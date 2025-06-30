import os
import sys
from dotenv import load_dotenv
from google import genai
from config import LLM_MODEL, MAX_ITERATIONS, SYSTEM_PROMPT
from google.genai import types
from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

if len(sys.argv) < 2:
    print("No prompt given!")
    sys.exit(1)

verbose = False
if len(sys.argv) > 2:
    if sys.argv[2] != "--verbose":
        print("Invalid argument, should be --verbose")
        sys.exit(1)
    verbose = True

prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file
    ]
)

client = genai.Client(api_key=api_key)

for iteration in range(MAX_ITERATIONS):
    response = client.models.generate_content(
        model = LLM_MODEL, 
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction = SYSTEM_PROMPT
            )
        )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            
            if (not function_call_result.parts or 
                not function_call_result.parts[0].function_response or 
                not function_call_result.parts[0].function_response.response):
                raise Exception("Error: No Result for called function")

            messages.append(function_call_result)

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)
        break

if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")