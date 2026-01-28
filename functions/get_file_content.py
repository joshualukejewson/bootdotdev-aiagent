import os.path


MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    try:
        cwd = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(cwd, file_path))
        valid_file_path = os.path.commonpath([cwd, full_file_path]) == cwd
        if not valid_file_path:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_file_path, "r") as file:
            file_contents = file.read(MAX_CHARS)
            if file.read(1):
                file_contents += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_contents

    except Exception:
        return "Error: general error while reading contents regarding sys module."
