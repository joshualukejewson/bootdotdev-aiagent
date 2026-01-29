import os.path
import subprocess
from google import genai
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    cwd = os.path.abspath(working_directory)
    full_file_path = os.path.abspath(os.path.join(cwd, file_path))
    valid_file_path = os.path.commonpath([cwd, full_file_path]) == cwd
    if not valid_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(full_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", full_file_path]
    if args:
        command.extend(args)

    try:
        completed_process = subprocess.run(
            command, capture_output=True, text=True, timeout=30
        )
        output_string = ""
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}"
        elif completed_process.stdout:
            output_string += f"STDOUT: {completed_process.stdout}"
        elif completed_process.stderr:
            output_string += f"STDERR: {completed_process.stderr}"
        else:
            output_string += "No output produced"

        return output_string
    except Exception as e:
        f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Builds a command python object from the supplied python file from file_path and creates a subprocess to execute the supplied file. Outputting to terminal upon success or failure.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to python file to be executed through the command line with the following supplied arguments.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of arguments to be given to the python file when running.",
            ),
        },
    ),
)
