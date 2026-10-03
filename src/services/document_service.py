from src.repositories.document_repo import create_document as create_document_repo
from sqlalchemy.orm import Session
from src.schemas.document import DocumentResponse
from fastapi import UploadFile
from src.services.file_storage import save_document
from pathlib import Path
from src.services.document_processing import extract_text_from_pdf
from src.services.chunking import chunk_text
from src.repositories.document_chunk_repo import create_document_chunks

async def create_document(db: Session, user_id:int, file: UploadFile) -> DocumentResponse:

    file_data = await save_document(file)

    try:
        document = create_document_repo(db, user_id, file_data)

        # Extract text from pdf
        pages = extract_text_from_pdf(document.filepath)
        # Retrived chunks
        chunks = []
        # Each Chunk Index
        chunk_index = 0

        for page in pages:
            # Extract page chunks
            page_chunks  = chunk_text(page["text"], 300, 50)
            # Extract chunks from page chunks
            for content in page_chunks:
                chunks.append({
                    "document_id": document.id,
                    "chunk_index": chunk_index,
                    "page_number": page["page_number"],
                    "content": content
                })

                chunk_index += 1

        # Bulk insert into document_chunks table
        create_document_chunks(db, chunks)

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

        file_path = Path(file_data["filepath"])

        if file_path.exists():
            file_path.unlink()

        raise