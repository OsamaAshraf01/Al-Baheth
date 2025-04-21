from models import File, Document
from models.document import FileMetadata
import hashlib
from typing import Optional, List, Dict, Any
from beanie import PydanticObjectId

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
    
    async def get_by_id(self, document_id: str) -> Optional[Document]:
        """
        Get a document by its ID.
        
        :param document_id: The ID of the document to retrieve.
        :return: Document object if found, None otherwise.
        """
        try:
            obj_id = PydanticObjectId(document_id)
            document = await Document.get(obj_id)
            return document
        except:
            return None
    
    async def update(self, document_id: str, update_data: Dict[str, Any]) -> Optional[Document]:
        """
        Update a document by its ID.
        
        :param document_id: The ID of the document to update.
        :param update_data: Dictionary containing the fields to update.
        :return: Updated Document object if found and updated, None otherwise.
        """
        try:
            document = await self.get_by_id(document_id)
            if not document:
                return None
                
            # Update only the allowed fields
            allowed_fields = ["title", "file_metadata"]
            for field in allowed_fields:
                if field in update_data:
                    setattr(document, field, update_data[field])
            
            await document.save()
            return document
        except Exception as e:
            print(f"Error updating document: {e}")
            return None
    
    async def delete(self, document_id: str) -> bool:
        """
        Delete a document by its ID.
        
        :param document_id: The ID of the document to delete.
        :return: True if the document was successfully deleted, False otherwise.
        """
        try:
            document = await self.get_by_id(document_id)
            if not document:
                return False
                
            await document.delete()
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    