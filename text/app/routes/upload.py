from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from googletrans import Translator, LANGUAGES
from fastapi.responses import JSONResponse, FileResponse
from typing import List

router = APIRouter()

# Initialize the translator
translator = Translator()

# To store translation history
history = []

# Endpoint to return supported languages
@router.get("/languages")
async def get_languages():
    # Return the available languages from googletrans
    return LANGUAGES

@router.post("/")
async def translate_file(file: UploadFile = File(...), language: str = Form(...)):
    # Read the file content
    contents = await file.read()
    text = contents.decode("utf-8")

    # Translate the text based on the selected language
    translated_text = translator.translate(text, src='auto', dest=language).text
    
    # Save the translation history with a unique ID
    history_item = {"id": len(history) + 1, "original": text, "translated": translated_text, "language": language}
    history.append(history_item)
    
    # Return the original and translated text
    download_url = f"/api/upload/download/{history_item['id']}"
    return {"original": text, "translated": translated_text, "language": language, "id": history_item["id"], "download_url": download_url}

@router.get("/history", response_model=List[dict])
async def get_history():
    return history

@router.get("/download/{history_id}")
async def download_history(history_id: int):
    # Find the translation by its ID
    item = next((item for item in history if item["id"] == history_id), None)
    if item:
        # Create a temporary file to store the translated text
        translated_text = item["translated"]
        file_path = f"translated_{history_id}.txt"
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(translated_text)
        
        # Return the file as a downloadable response
        return FileResponse(file_path, media_type='text/plain', filename=f"translated_{history_id}.txt")
    
    return JSONResponse(status_code=404, content={"error": "History item not found"})

@router.delete("/delete/{history_id}")
async def delete_history(history_id: int):
    global history  # Access the global history list
    # Find the index of the item to delete
    item_index = next((index for index, item in enumerate(history) if item["id"] == history_id), None)
    if item_index is not None:
        # Remove the item from the history
        deleted_item = history.pop(item_index)
        return {"message": "Translation deleted successfully", "deleted_item": deleted_item}
    raise HTTPException(status_code=404, detail="History item not found")
