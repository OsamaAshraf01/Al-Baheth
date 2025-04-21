from typing_extensions import Annotated
from beanie import Document as BeanieDocument, Indexed
from pydantic import BaseModel

class FileMetadata(BaseModel):
    filename: str
    content_type: str
    size: int

class Document(BeanieDocument):
    file_metadata: FileMetadata
    title: str
    hashed_content : Annotated[str, Indexed(unique=True)]
    
    
    class Settings:
        collection = "corpus"