from models import File, Document
from models.document import FileMetadata
import hashlib
from typing import Optional

class DocumentRepository:

    async def create(self, file: File, content : str) -> Optional[Document]:
        """
        Create a new document in the database from the file.
        
        :param file: File object containing the file information.
        :return: Document object created from the file.
        """
        hashed_content = hashlib.sha256(content.encode()).hexdigest()
        
        found = await self.get_by_key(hashed_content)
        if found:
            return None
        
        file_metadata = FileMetadata(
            filename=file.file.filename, 
            content_type=file.file.content_type,
            size=file.file.size
        )
        
        document = Document(
            file_metadata=file_metadata, 
            title=file.file.filename, 
            hashed_content=hashed_content
        )
        
        await document.insert()
        return document
    
    async def get_by_key(self, key: str) -> Optional[Document]:
        """
        Get a document by its hashed content.
        
        :param hashing_key: The hashed content of the document.
        :return: Document object if found, None otherwise.
        """
        document = await Document.find_one(Document.hashed_content == key)
        return document