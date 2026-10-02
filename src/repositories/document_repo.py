from sqlalchemy.orm import Session
from sqlalchemy import Select

from src.models.document import Document

def create_document(db: Session, user_id:int, file_data:dict) -> Document:

    document = Document(
        user_id = user_id,
        filename = file_data["filename"],
        filesize = file_data["filesize"],
        filepath = file_data["filepath"],
        content_type = file_data["content_type"]
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document