import os
from fastapi import HTTPException

ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def validate_file(filename: str, size: int, content_type: str):
    """Validate file extension, size, and MIME type."""
    ext = filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file extension. Only PDF allowed.")
    
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Max 100MB.")
    
    if content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid MIME type. Expected application/pdf.")

def is_scanned_pdf(file_path: str) -> bool:
    """Check if PDF has text layer using poppler-utils (pdftotext)."""
    import subprocess
    try:
        # Check if there is any text in the first 5 pages
        result = subprocess.run(
            ["pdftotext", "-l", "5", file_path, "-"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return not result.stdout.strip()
    except Exception:
        return False  # Fail-safe
