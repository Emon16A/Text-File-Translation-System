from app.services.websocket_manager import manager  # Import the WebSocket manager
from app.utils.file_handler import save_file  # Import save_file function
from app.services.translation_metadata import save_translation_metadata  # Assuming this function exists
from googletrans import Translator  # Import the translator

translator = Translator()

async def translate_text(file_path, language, session_id, file_name):
    """Translate the content of the file and save it."""
    try:
        # Send the starting message
        await manager.send_message(session_id, "Starting translation...")

        # Read the content from the file
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Attempt translation with error handling
        try:
            # Translate the text (auto-detect the source language)
            translated = translator.translate(text, src='auto', dest=language)
            translated_content = translated.text
        except Exception as e:
            # If translation fails, log the error and use the original text
            print(f"Error occurred during translation: {str(e)}")
            translated_content = text  # Fallback to original text

        new_file_path = f"{file_path}.translated"  # Path for the translated file

        # Save the translated content to a new file
        save_file(translated_content, new_file_path)

        # Notify WebSocket that translation is complete
        await manager.send_message(session_id, "Translation completed! File is ready for download.")

        # Save translation status
        await save_translation_metadata(session_id, file_name, "Completed")

        return new_file_path  # Optionally return the new file path
    except Exception as e:
        # In case of error, notify the WebSocket and raise the exception
        await manager.send_message(session_id, f"Error during translation: {e}")
        raise
