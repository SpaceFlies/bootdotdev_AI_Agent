import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        #print(os.listdir(target_dir))
        result = []
        for item in os.listdir(target_dir):
            result += [f" - {item}, file_size={os.path.getsize(f"{target_dir}/{item}")} bytes, is_dir={os.path.isdir(f"{target_dir}/{item}")}"]
        return "\n".join(result)
    except Exception as err:
        return f"Error: {err}"

#print(get_files_info("calculator", "."))
#get_files_info("calculator", ".")