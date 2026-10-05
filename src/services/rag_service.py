from sqlalchemy.orm import Session

from src.services.embedding import generate_embedding
from src.repositories.chunk_embedding_repo import search_similar_chunks
from src.services.context_builder import build_context
from src.services.llm import generate_answer

def ask_question(db:Session, document_id:int, question:str, user_id:int):
    query_embedding = generate_embedding(question)

    if not query_embedding:
        raise ValueError("Failed to generate query embedding")

    relevant_chunks = search_similar_chunks(db, user_id, document_id, query_embedding, 5)

    if not relevant_chunks:
        return []

    context = build_context(relevant_chunks)

    return generate_answer(question, context)
    

