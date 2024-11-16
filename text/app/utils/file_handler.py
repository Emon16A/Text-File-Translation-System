# app/utils/file_handler.py

def save_file(file, destination):
    with open(destination, "wb") as f:
        f.write(file.file.read())

def load_file(file_path):
    with open(file_path, "r") as f:
        return f.read()
