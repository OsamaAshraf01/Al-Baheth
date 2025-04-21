from fastapi import UploadFile
from typing_extensions import Annotated
from beanie import Document as BeanieDocument, Indexed

class Document(BeanieDocument):
    file: UploadFile
    title: str
    hashed_content : Annotated[str, Indexed(unique=True)]
    
    
    class Settings:
        collection = "corpus"