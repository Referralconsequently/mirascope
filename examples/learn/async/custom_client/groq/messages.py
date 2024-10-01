from groq import AsyncGroq
from mirascope.core import Messages, groq


@groq.call("llama-3.1-8b-instant", client=AsyncGroq())
async def recommend_book_async(genre: str) -> Messages.Type:
    return Messages.User(f"Recommend a {genre} book")
