from src.core.config import settings

from FlagEmbedding import BGEM3FlagModel

from functools import lru_cache

@lru_cache(maxsize=1)
def get_embedding_model() -> BGEM3FlagModel:
    return BGEM3FlagModel(
        settings.EMBEDDING_MODEL,
        use_fp16=settings.EMBEDDING_USE_FP16
    )

def generate_embedding(text: str) -> list[float]:
    model = get_embedding_model()

    output = model.encode(text)

    embedding = output["dense_vecs"]
    
    return embedding.tolist()