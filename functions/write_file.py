import os
from google.genai import types
from functions.validate_directory_path import validate_directory_path

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the content into a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write or overwrite the content into, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that get written into the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    errMsg = f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
    full_file_path, error = validate_directory_path(working_directory, file_path, errMsg)

    if error:
        return error

    try:
        dir_path = os.path.dirname(full_file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(full_file_path, "w") as file:
            file.write(content)

        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as ex:
        return f"Error: Unexpected {ex=}, {type(ex)=}"