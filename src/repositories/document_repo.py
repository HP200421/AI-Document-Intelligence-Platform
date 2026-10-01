from sqlalchemy.orm import Session
from sqlalchemy import Select

from src.models.document import Document
from src.schemas.document import DocumentCreate

def create_document(db: Session, document_data:DocumentCreate) -> Document:

    document = Document(
        filename = document_data.filename,
        filesize = document_data.filesize,
        filepath = document_data.filepath,
        content_type = document_data.content_type
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document