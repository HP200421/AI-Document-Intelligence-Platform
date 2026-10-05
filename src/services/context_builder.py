def build_context(retrieved_chunks:list[dict]) -> str:
    context_parts = []

    for chunk in retrieved_chunks:
        content = chunk.get("content")
        page_number = chunk.get("page_number")

        if not content:
            continue

        if page_number is not None:
            context_parts.append(
                f"[Page {page_number}]\n{content}"
            )
        else:
            context_parts.append(content)



    return "\n\n".join(context_parts)