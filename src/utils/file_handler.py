def read_file(file_path):
    """Reads the contents of a file and returns it as a string."""
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Writes the given content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)

def file_exists(file_path):
    """Checks if a file exists at the given path."""
    import os
    return os.path.isfile(file_path)

def get_file_extension(file_path):
    """Returns the file extension of the given file."""
    import os
    return os.path.splitext(file_path)[1]

def create_directory(directory_path):
    """Creates a directory if it does not exist."""
    import os
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)