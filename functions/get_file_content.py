import os

from google import genai
from google.genai import types

from config import MAX_CHARS


# Return the contents of a file under working_directory
def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        # If the path escapes the working directory, return a permission error
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # If the path isn’t a regular file, return a not-found error
        elif not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Open the file for reading and limit how much we load into memory
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        # Return the collected file contents (possibly with a truncation note)
        return file_content_string

    # On any unexpected error, return a standardized error string
    except Exception as e:
        return f"Error: {e}"


# Schema describing get_file_content function signature for LLM tool calling
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file at the given path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read",
            ),
        },
        required=["file_path"],
    ),
)
