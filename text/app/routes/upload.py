from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from googletrans import Translator, LANGUAGES
from fastapi.responses import JSONResponse, FileResponse
from typing import List

router = APIRouter()

translator = Translator()
history = []

def chunk_text(text: str, chunk_size: int = 5000):
    """Splits the text into smaller chunks of a given size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

@router.get("/languages")
async def get_languages():
    """Returns the available languages."""
    return LANGUAGES

@router.post("/")
async def translate_file(file: UploadFile = File(...), language: str = Form(...)):
    """Uploads and translates a file."""
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # Read in 1MB chunks
                f.write(chunk)

        # Read file contents
        with open(temp_file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Split the text into chunks and translate
        chunks = chunk_text(text)
        translated_text = ""
        for chunk in chunks:
            translated_chunk = translator.translate(chunk, src='auto', dest=language).text
            translated_text += translated_chunk

        # Save translation to history
        history_item = {"id": len(history) + 1, "original": text, "translated": translated_text, "language": language}
        history.append(history_item)

        # Provide download link
        download_url = f"/api/upload/download/{history_item['id']}"
        return {"original": text, "translated": translated_text, "language": language, "id": history_item["id"], "download_url": download_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the file: {str(e)}")

@router.get("/history", response_model=List[dict])
async def get_history():
    """Returns the translation history."""
    return history

@router.get("/download/{history_id}")
async def download_history(history_id: int):
    """Downloads translated content based on history ID."""
    item = next((item for item in history if item["id"] == history_id), None)
    if item:
        file_path = f"translated_{history_id}.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(item["translated"])
        return FileResponse(file_path, media_type="text/plain", filename=f"translated_{history_id}.txt")
    return JSONResponse(status_code=404, content={"error": "History item not found"})

@router.delete("/delete/{history_id}")
async def delete_history(history_id: int):
    """Deletes a history item by ID."""
    global history
    item_index = next((index for index, item in enumerate(history) if item["id"] == history_id), None)
    if item_index is not None:
        deleted_item = history.pop(item_index)
        return {"message": "Translation deleted successfully", "deleted_item": deleted_item}
    raise HTTPException(status_code=404, detail="History item not found")
