from beanie import Document as BeanieDocument, Indexed
from typing_extensions import Annotated


class Document(BeanieDocument):
    hashed_content: Annotated[str, Indexed(unique=True)]
    title: str
    parsed_text: str
    embeddings: list[float]
    bytes_content: bytes | None

    class Settings:
        collection = "corpus"
