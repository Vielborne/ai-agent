import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for name in os.listdir(target_dir):
            complete_path = os.path.join(target_dir, name)
            is_dir = os.path.isdir(complete_path)
            size = os.path.getsize(complete_path)
            line = f"{name}: file_size={size}, is_dir={is_dir}"
            lines.append(line)

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
