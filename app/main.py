import os
import uuid
import logging
import time
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# 1. Configure root_path using environment variable ROOT_PATH
# Behind Nginx at /docai, set ROOT_PATH="/docai". Locally, leave it empty.
ROOT_PATH = os.environ.get("ROOT_PATH", "")

app = FastAPI(
    title="DocAI | High-Fidelity PDF Watermark Remover",
    root_path=ROOT_PATH
)

# 2. Configure StaticFiles properly
# BASE_DIR centers paths relative to this main.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 3. Configure Jinja2Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Import business logic
from app.storage import storage
from app.converter import process_conversion

# Constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_MIME_TYPES = ["application/pdf"]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Ensure request object is passed to enable request.url_for in templates
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_id = str(uuid.uuid4())
    filename = f"{file_id}.pdf"

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Max 100MB.")
    
    from io import BytesIO
    storage.save(BytesIO(content), filename, bucket="input")
    background_tasks.add_task(process_conversion, file_id)
    
    return {"file_id": file_id, "status": "processing"}

@app.api_route("/download/{file_id}", methods=["GET", "HEAD"])
async def download_document(file_id: str):
    if not storage.exists(file_id, bucket="output"):
        raise HTTPException(status_code=404, detail="Processing or not found.")
    
    from app.storage.local import LocalStorageProvider
    if isinstance(storage, LocalStorageProvider):
        path = storage.get_path(file_id, "pdf", bucket="output")
        return FileResponse(
            path=path,
            media_type="application/pdf",
            filename=f"converted_{file_id}.pdf"
        )
    else:
        from fastapi.responses import RedirectResponse
        url = storage.get_download_url(file_id)
        return RedirectResponse(url)

async def cleanup_old_files():
    from app.storage.local import LocalStorageProvider
    if not isinstance(storage, LocalStorageProvider):
        return
    now = time.time()
    for bucket in ["input", "output"]:
        dir_path = storage.input_dir if bucket == "input" else storage.output_dir
        for f in os.listdir(dir_path):
            file_path = os.path.join(dir_path, f)
            if os.path.getmtime(file_path) < now - (24 * 3600):
                try:
                    os.remove(file_path)
                    logger.info(f"Auto-deleted old file: {f}")
                except:
                    pass

@app.on_event("startup")
async def startup():
    logger.info(f"DocAI Starting up with ROOT_PATH: '{ROOT_PATH}'")
    import asyncio
    asyncio.create_task(cleanup_old_files())

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
