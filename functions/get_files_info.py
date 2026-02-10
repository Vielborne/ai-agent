import os


# Return the info of files under working_directory
def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        # If the path escapes the working directory, return a permission error
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # If the path doesn't point to an existing directory, return an error
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Build a list of formatted strings describing each item in the directory
        lines = []
        for name in os.listdir(target_dir):
            complete_path = os.path.join(target_dir, name)
            is_dir = os.path.isdir(complete_path)
            size = os.path.getsize(complete_path)
            line = f"{name}: file_size={size}, is_dir={is_dir}"
            lines.append(line)

        # Join all lines and return the result
        return "\n".join(lines)

    # On any unexpected error, return a standardized error string
    except Exception as e:
        return f"Error: {e}"
