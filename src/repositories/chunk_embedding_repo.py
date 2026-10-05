from sqlalchemy.orm import Session
from src.models.chunk_embedding import ChunkEmbedding
from src.models.document_chunk import DocumentChunk
from src.models.document import Document
from sqlalchemy import Select

def create_chunk_embeddings(db:Session, chunk_embeddings_data:list[dict]):
    chunk_embeddings = [
        ChunkEmbedding(**data)
        for data in chunk_embeddings_data
    ]

    db.add_all(chunk_embeddings)
    db.commit()

    return chunk_embeddings

def search_similar_chunks(db: Session, user_id:int, document_id:int, query_embedding:list[float], top_k:int=10):
    distance = ChunkEmbedding.embedding.cosine_distance(query_embedding)

    stmt = (
        Select(
            DocumentChunk.id.label("chunk_id"),
            DocumentChunk.content,
            DocumentChunk.page_number,
            distance.label("distance")
        )
        .join(
            ChunkEmbedding,
            ChunkEmbedding.chunk_id == DocumentChunk.id 
        )
        .join(
            Document,
            Document.id == DocumentChunk.document_id
        )
        .where(
            Document.id == document_id,
            Document.user_id == user_id
        )
        .order_by(distance)
        .limit(top_k)
    )

    result = db.execute(stmt)

    return result.all()