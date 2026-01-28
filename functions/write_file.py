import os.path


def write_file(working_directory, file_path, content):
    cwd = os.path.abspath(working_directory)
    full_file_path = os.path.abspath(os.path.join(cwd, file_path))
    valid_file_path = os.path.commonpath([cwd, full_file_path]) == cwd
    if not valid_file_path:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(full_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        with open(full_file_path, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: unable to write content to given file ({e})."
