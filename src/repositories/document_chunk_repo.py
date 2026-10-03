from sqlalchemy.orm import Session
from src.models.document_chunk import DocumentChunk

def create_document_chunks(db: Session, document_chunk_data:list[dict]):
    document_chunks = [
        DocumentChunk(**data)
        for data in document_chunk_data
    ]

    db.add_all(document_chunks)
    db.commit

    return document_chunks
