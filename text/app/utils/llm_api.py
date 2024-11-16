import time
def translate_text(file_path, target_language):
    time.sleep(5)  # Simulate processing
    with open(file_path, "r") as file:
        content = file.read()
    translated_content = f"[Translated to {target_language}]: {content}"
    with open(f"{file_path}.translated.txt", "w") as file:
        file.write(translated_content)
