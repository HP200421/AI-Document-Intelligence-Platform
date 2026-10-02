from src.repositories.document_repo import create_document as create_document_repo
from sqlalchemy.orm import Session
from src.schemas.document import DocumentResponse
from fastapi import UploadFile
from src.services.file_storage import save_document
from pathlib import Path

async def create_document(db: Session, user_id:int, file: UploadFile) -> DocumentResponse:

    file_data = await save_document(file)

    try:
        document = create_document_repo(db, user_id, file_data)

        return DocumentResponse(
            id = document.id,
            filename = document.filename,
            filepath = document.filepath,
            content_type = document.content_type,
            created_at = document.created_at,
            updated_at = document.updated_at,
        )
    except Exception:
        # If database transaction fails, we need to remove the stored file
        # No orphaned records should be there

        file_path = Path(file_data["file_path"])

        if file_path.exists():
            file_path.unlink()

        raise