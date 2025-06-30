import os
from google.genai import types
from config import MAX_CHARS
from functions.validate_directory_path import validate_directory_path

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Delivers the content from a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get the content from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    full_file_path, error = validate_directory_path(working_directory, file_path)
    if error:
        return error
    
    if not os.path.isfile(full_file_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""
    
    try:
        with open(full_file_path, "r") as file:
            content = file.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += f"[...File \"{file_path}\" truncated at 10000 characters]"
            return content
    except Exception as ex:
        return f"Error: Unexpected {ex=}, {type(ex)=}"