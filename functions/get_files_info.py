import os

def get_files_info(working_directory, directory=None):
    working_dir_abs_path = os.path.abspath(working_directory)
    working_dir_cont = os.listdir(working_dir_abs_path)
    print(working_dir_cont)

get_files_info(working_directory='calculator', directory="pkg")