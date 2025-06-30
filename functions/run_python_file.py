import os
import subprocess
from google.genai import types
from functions.validate_directory_path import validate_directory_path

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the code from a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The runnable python file, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    errMsg = f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    full_file_path, error = validate_directory_path(working_directory, file_path, errMsg)

    if error:
        return error
    
    try:
        if not full_file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file."

        if not os.path.exists(full_file_path):
            return f"Error: File \"{file_path}\" not found."
        
        dir_path = os.path.dirname(full_file_path)
        completed = subprocess.run(['python3.13', full_file_path], timeout = 30, capture_output = True, cwd = dir_path)
        
        if completed.stdout == "" and completed.stderr == "":
            return "No output produced."

        result = f"STDOUT: {completed.stdout}STDERR: {completed.stderr}"
        if completed.returncode != 0:
            result += f"Process exited with code {completed.returncode}"
        return result
    except Exception as ex:
        return f"Error: Executing Python file: {ex=}, {type(ex)=}"