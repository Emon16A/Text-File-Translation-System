from pathlib import Path

# Function to read the content of the uploaded file
def read_text_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

# Function to save the translated text to a new file
def save_translated_file(translated_text: str, output_file_path: str):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)
    except Exception as e:
        print(f"Error saving file {output_file_path}: {e}")
