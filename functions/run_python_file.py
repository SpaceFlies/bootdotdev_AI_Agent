import os
import sys
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        root, ext = os.path.splitext(target_file)
        return_string = ""
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
             
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        elif ext != ".py":
            return f'Error: "{target_file}" is not a Python file'
        
        else:
            command = ["python3", target_file]
            if args:
                command.extend(args)

            process_result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            return_string = f"STDOUT: {process_result.stdout}\nSTDERR: {process_result.stderr}"
            
            if process_result.returncode != 0:
                return_string = f"Process exited with code: {process_result.returncode}\n" + return_string
                
            
            if not process_result.stdout and not process_result.stderr:
                print("No output produced")
                return 
                
                
        print(return_string)
        
    except Exception as err:
        return f"Error: executing Python file: {err}"
    
run_python_file("calculator", "../main.py") #(this should return an error)
#run_python_file("calculator", "main.py") #(should print the calculator's usage instructions)