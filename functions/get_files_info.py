import os.path


def get_files_info(working_directory, directory="."):
    cwd = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(cwd, directory))
    valid_target_dir = os.path.commonpath([cwd, target_dir]) == cwd
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        directory_listing = ""
        for item in os.listdir(target_dir):
            name = item
            size = os.path.getsize(os.path.join(target_dir, item))
            is_dir = os.path.isdir(os.path.join(target_dir, item))

            directory_listing = "".join(
                [
                    directory_listing,
                    f"- {name}: file_size={size} bytes, is_dir={is_dir}\n",
                ]
            )
        return directory_listing.strip("\n")
    except Exception:
        return "Error: cannot read details of file or directory."
