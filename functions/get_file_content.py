import os

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.join(working_dir_abs_path, file_path)
        if working_dir_abs_path not in file_path_abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(os.path.join(working_dir_abs_path, file_path)):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        MAX_CHARS = 10000
        with open(os.path.join(working_dir_abs_path, file_path), "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return file_content_string
    except Exception as e:
        return f'Error: {str(e)}'