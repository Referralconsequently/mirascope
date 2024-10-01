import asyncio

from mirascope.core import Messages, azure


@azure.call(model="gpt-4o-mini")
async def recommend_book(genre: str) -> Messages.Type:
    return Messages.User(f"Recommend a {genre} book")


async def main():
    response = await recommend_book("fantasy")
    print(response.content)


asyncio.run(main())
