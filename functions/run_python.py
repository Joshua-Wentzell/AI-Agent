import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.join(working_dir_abs_path, file_path)
        if working_dir_abs_path not in file_path_abs_path or ".." in file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(file_path_abs_path):
            return f'Error: File "{file_path}" not found.'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'
        filename = os.path.basename(file_path_abs_path)
        directory_path = os.path.dirname(file_path_abs_path)
        completed_process = subprocess.run([f"python3 {file_path}"], capture_output=True, timeout=30, cwd=directory_path, shell=True)
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout == "":
            return "No output produced."
        return f"STDOUT:{completed_process.stdout}\nSTDERR:{completed_process.stderr}"
    except Exception as e:
        return f'Error: {str(e)}'