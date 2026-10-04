from sqlalchemy.orm import Session
from src.models.chunk_embedding import ChunkEmbedding

def create_chunk_embeddings(db:Session, chunk_embeddings_data:list[dict]):
    chunk_embeddings = [
        ChunkEmbedding(**data)
        for data in chunk_embeddings_data
    ]

    db.add_all(chunk_embeddings)
    db.commit()

    return chunk_embeddings