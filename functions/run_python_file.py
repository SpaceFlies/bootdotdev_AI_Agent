import os
import sys
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=("runs a python file with optional arguments like 'run main.py'"),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file that needs to be run and executed, relative to the working directory. (default is the working directory itself)",
                
                ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to be passed for executing the python file.",
                items=types.Schema(
                    type=types.Type.STRING),
                ),
            
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        root, ext = os.path.splitext(target_file)
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif ext != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        else:
            command = ["python", target_file]
            if args:
                command.extend(args)

            process_result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            return_string = f"STDOUT: {process_result.stdout}\nSTDERR: {process_result.stderr}"
            
            if process_result.returncode != 0:
                return_string = f"Process exited with code: {process_result.returncode}\n" + return_string
                
            
            if not process_result.stdout and not process_result.stderr:
                print("No output produced")
                return 
                
                
        return return_string
        
    except Exception as err:
        return f"Error: executing Python file: {err}"
    
#print(run_python_file("calculator", "../main.py")) #(this should return an error)
#run_python_file("calculator", "main.py") #(should print the calculator's usage instructions)