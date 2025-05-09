from beanie import Document as BeanieDocument, Indexed
from typing_extensions import Annotated


class Document(BeanieDocument):
    hashed_content: Annotated[str, Indexed(unique=True)]
    original_content: str
    processed_content: str
    title: str

    class Settings:
        collection = "corpus"
