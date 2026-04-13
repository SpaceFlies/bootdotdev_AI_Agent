import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "This function ONLY returns metadata about files (name, size, and whether each item is a directory). "
        "It does NOT read, open, execute, or modify any files. "
        "Use this function ONLY when the user wants to inspect the contents of a folder."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Directory path to list files from, relative to the working directory. "
                    "Defaults to the working directory."
                ),
            ),
        },
    ),
)

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
        #print("\n".join(result))
        return "\n".join(result)
    except Exception as err:
        return f"Error: {err}"