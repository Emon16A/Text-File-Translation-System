from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, download, history, websocket, languages
import os

app = FastAPI()

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routes
app.include_router(upload.router, prefix="/api/upload")
app.include_router(download.router, prefix="/api/download")
app.include_router(history.router, prefix="/api/history")
app.include_router(websocket.router, prefix="/ws")
app.include_router(languages.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def root():
    template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates", "index.html")
    if not os.path.exists(template_path):
        return HTMLResponse(content="<h1>404: Template Not Found</h1>", status_code=404)
    with open(template_path, "r") as f:
        return f.read()

@app.head("/", response_class=HTMLResponse)
async def head_root():
    return HTMLResponse(status_code=200)
