import os


# Write or overwrite the content of a file under working directory
def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        # If the path escapes the working directory, return a permission error
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        # # If the path points to an existing directory, return a permission error
        elif os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure all parent directories exist before attempting to open the file
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        # Open the file for writing and overwrite its content
        with open(target_dir, "w") as f:
            f.write(content)

        # Return a success message with character count
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    # On any unexpected error, return a standardized error string
    except Exception as e:
        return f"Error: {e}"
