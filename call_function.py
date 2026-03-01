from google import genai
from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

# Tool wrapper containing all function declarations available to the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)


def call_function(function_call, verbose=False):
    # Print the function call (print args only in verbose mode)
    if verbose is True:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # Map function names to callable functions
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    # Get the function name as a string
    function_name = function_call.name or ""
    if function_name not in function_map:
        # Return an error response for unknown function names
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Copy provided args or use an empty dict
    args = dict(function_call.args) if function_call.args else {}
    # Set the working directory for the tool call
    args["working_directory"] = "./calculator"
    # Selected function called with keyword arguments
    function_result = function_map[function_name](**args)

    # Return the function result
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
