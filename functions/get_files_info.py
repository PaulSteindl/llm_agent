import os
from google.genai import types
from functions.validate_directory_path import validate_directory_path

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    full_file_path, error = validate_directory_path(working_directory, directory)
    if error:
        return error

    if not os.path.isdir(full_file_path):
        return f"Error: \"{directory}\" is not a directory"

    try:
        result = ""
        for entity in os.listdir(full_file_path):
            entity_path = os.path.join(full_file_path, entity)
            file_size = os.path.getsize(entity_path)
            is_dir = os.path.isdir(entity_path)
            result += f"- {entity}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return result
    except FileNotFoundError as ex:
        return f"Error: File {entity_path}, does not exist. {ex=}"
    except Exception as ex:
        return f"Error: Unexpected {ex=}, {type(ex)=}"
