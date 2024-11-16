import os

UPLOAD_DIR = "uploads"
TRANSLATED_DIR = "translated"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSLATED_DIR, exist_ok=True)

def save_file(file):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def get_translated_file_path(file_id):
    return os.path.join(TRANSLATED_DIR, file_id)
