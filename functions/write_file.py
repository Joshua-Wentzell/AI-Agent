import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.join(working_dir_abs_path, file_path)
        if working_dir_abs_path not in file_path_abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(file_path_abs_path):
            with open(file_path_abs_path, "x") as f:
                f.write(content)
        else:
            with open(file_path_abs_path, "w") as f:
                f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'