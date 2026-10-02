from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR = Path("storage/documents")
ALLOWED_CONTENT_TYPES = {"application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024 #10 MB

class FileStorageException(Exception):
    pass

async def save_document(file: UploadFile) -> dict:
    # Check content type of uploaded file
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise FileStorageException("Only PDF files are allowed")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension != ".pdf":
        raise FileStorageException("Only PDF files are allowed")

    stored_filename = f"{uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / stored_filename

    file_size = 0
    try:
        with file_path.open("wb") as destination:
            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise FileStorageException("File size must not exceed 10 MB")

                destination.write(chunk)
    except:
        if file_path.exists():
            file_path.unlink()

        raise

    finally:
        await file.close()

    return {
        "filename": file.filename,
        "filepath": str(file_path),
        "filesize": file_size,
        "content_type": file.content_type
    }

