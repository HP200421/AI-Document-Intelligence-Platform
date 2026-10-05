from sqlalchemy.orm import Session

from src.services.embedding import generate_embedding
from src.repositories.chunk_embedding_repo import search_similar_chunks

def ask_question(db:Session, document_id:int, question:str, user_id:int):
    query_embedding = generate_embedding(question)

    if not query_embedding:
        raise ValueError("Failed to generate query embedding")

    relevant_chunks = search_similar_chunks(db, user_id, document_id, query_embedding, 5)

    if not relevant_chunks:
        return []
    
    return relevant_chunks

