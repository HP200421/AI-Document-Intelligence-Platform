from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from src.schemas.document import DocumentResponse
from src.services.document_service import create_document
from src.db.database import get_db
from src.api.deps import get_current_user

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document_endpoint(file:UploadFile = File(...), user_id:int = Depends(get_current_user),db: Session = Depends(get_db)):

    return await create_document(db, user_id, file)