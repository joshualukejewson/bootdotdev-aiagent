import os.path
from google import genai
from google.genai import types


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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the file contents that are supplied to the file given via the file path that is relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to be written to, overwriting the previous contents of the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String of file contents that are to be written to the file.",
            ),
        },
    ),
)
