def chunk_text(text: str, chunk_size:int = 1000, overlap:int=200) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("Chunk Size must be greater than 0")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative")

    if chunk_size < overlap:
        raise ValueError("Overlap must be smaller than Chunk Size")

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
    