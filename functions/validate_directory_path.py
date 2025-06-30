import os

def validate_directory_path(working_directory, entity, customErr = None):
    absolut_working_dir = os.path.abspath(working_directory)
    target = absolut_working_dir
    if entity:
        target = os.path.abspath(os.path.join(working_directory, entity))

    if not target.startswith(absolut_working_dir):
        if not customErr:
            return None, f"Error: Cannot list \"{target}\" as it is outside the permitted working directory"
        return None, customErr
    
    return target, None