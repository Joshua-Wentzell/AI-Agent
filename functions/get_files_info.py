import os

def get_files_info(working_directory, directory=None):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        working_dir_cont = os.listdir(working_dir_abs_path)
        if directory:
            if directory == ".":
                dir_contents_str = ''.join(list(map(lambda x: f"- {x}: file_size={os.path.getsize(os.path.join(working_dir_abs_path, x))} bytes, is_dir={os.path.isdir(os.path.join(working_dir_abs_path, x))}", os.listdir(working_dir_abs_path))))
                return dir_contents_str
            if directory not in working_dir_cont:
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            elif not os.path.isdir(os.path.join(working_dir_abs_path, directory)):
                return f'Error: "{directory}" is not a directory'
            dir_contents_str = ''.join(list(map(lambda x: f"- {x}: file_size={os.path.getsize(os.path.join(working_dir_abs_path, directory, x))} bytes, is_dir={os.path.isdir(os.path.join(working_dir_abs_path, directory, x))}", os.listdir(os.path.join(working_dir_abs_path, directory)))))
            return dir_contents_str
    except Exception as e:
        return f'Error: {str(e)}'