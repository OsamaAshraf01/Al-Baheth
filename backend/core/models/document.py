from fastapi import UploadFile
from beanie import Document as BeanieDocument

class Document(BeanieDocument):
    file: UploadFile
    title: str
    
    
    class Settings:
        collection = "corpus"