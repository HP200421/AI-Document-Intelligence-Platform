from openai import OpenAI
from src.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_answer(question:str, context:str) ->str:
    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        instructions=( "You are a document question-answering assistant. " "Answer the user's question using only the provided context. " "If the answer cannot be found in the context, " "say that the information is not available in the document. " "Do not make up information." ),
        input=( f"Context:\n" f"{context}\n\n" f"Question:\n" f"{question}" )
    )

    return response.output.text