from typing_extensions import Annotated
from beanie import Document as BeanieDocument, Indexed
from pydantic import Field

class Document(BeanieDocument):
    hashed_content : Annotated[str, Indexed(unique=True)]
    content_type: str
    data: bytes = Field(...)
    title: str
    
    class Settings:
        collection = "corpus"