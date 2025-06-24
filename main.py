import os
import sys
from google.genai import types
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

verbose = False
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key = api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get the content from, relative to the working directory.",
            ),
        },
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run, relative to the working directory.",
            ),
        },
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to a new file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to create, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The file content to add to the new file.",
            ),
        },
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    if function_call_part is None:
        print("No function call part found")
        return

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    functions_available = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if function_call_part.name in functions_available.keys():
        result = functions_available[function_call_part.name](working_directory="./calculator", **function_call_part.args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

if len(sys.argv) > 1:
    prompt = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
               verbose = True 
else:
    sys.exit(1)
messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),]

MAX_CALLS = 20
i = 0
while (i < 20):
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt))
    if response.function_calls and response.candidates[0].content.parts[0].function_call:
        for candidate in response.candidates:
            messages.append(candidate.content)
        result = call_function(response.candidates[0].content.parts[0].function_call, verbose)
        if result:
            messages.append(result)
            if result.parts[0].function_response.response:
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception("FATAL: no result from the function call")
    else:
        print(response.text)
        break
    i += 1



if verbose:
    print(f"User prompt: {prompt}")
    if response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")