from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from src.schemas.document import DocumentResponse
from src.services.document_service import create_document
from src.db.database import get_db
from src.api.deps import get_current_user
from src.services.rag_service import ask_question

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document_endpoint(file:UploadFile = File(...), user_id:int = Depends(get_current_user),db: Session = Depends(get_db)):

    return await create_document(db, user_id, file)

@router.post("/{document_id}/ask")
async def ask_document_question(question:str, document_id:int, db: Session = Depends(get_db), user_id:int = Depends(get_current_user)):
    
    return ask_question(db, document_id, question, user_id)