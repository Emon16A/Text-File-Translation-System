from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Pydantic models to define the structure of the session data and files
class FileObject(BaseModel):
    fileName: str
    filePath: str
    processedAt: datetime
    result: str

class Session(BaseModel):
    sessionId: str
    createdAt: datetime
    filesProcessed: List[FileObject]
