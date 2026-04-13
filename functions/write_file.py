import os
def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        #Create directory
        

        with open(target_file, "r") as f:
            MAX_CHARS = 10_000 #change this to import from config.py
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'


        
        return content


    except Exception as err:
        return f"Error: {err}"