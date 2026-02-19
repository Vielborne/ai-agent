import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        # If the path escapes the working directory, return a permission error
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # If the path isn’t a regular file, return a not-found error
        elif not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        # If the path isn’t a python file, return a not-python file error
        elif not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Command that will be used to run the file
        command = ["python", target_dir]
        # If extra CLI args provided, append them to the command
        if args:
            command.extend(args)

        # Command is run as a child process
        completed_process_object = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        output = ""
        # If the program exited with an error code
        if completed_process_object.returncode != 0:
            output += f"Process exited with code {completed_process_object.returncode}"
        # If nothing was printed to stdout AND nothing was printed to stderr
        if not completed_process_object.stdout and not completed_process_object.stderr:
            output += "No output produced"
        # If there is standard output
        if completed_process_object.stdout:
            output += f"STDOUT: {completed_process_object.stdout}"
        # If there is standard error output
        if completed_process_object.stderr:
            output += f"STDERR: {completed_process_object.stderr}"

        # Return combined output string
        return output

    # On any unexpected error, return a standardized error string
    except Exception as e:
        return f"Error: executing Python file: {e}"
