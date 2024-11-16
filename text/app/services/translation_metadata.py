from datetime import datetime
from app.models import files_collection  

async def save_translation_metadata(session_id, file_name, status):
    """Store metadata about the translation process in a database (e.g., MongoDB)."""
    try:
        # Store metadata in the database
        await files_collection.insert_one({
            "session_id": session_id,
            "file_name": file_name,
            "status": status,
            "created_at": datetime.utcnow()
        })
    except Exception as e:
        print(f"Error saving metadata: {e}")
        raise
