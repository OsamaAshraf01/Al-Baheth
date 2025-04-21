from models import File, Document
from models.document import FileMetadata
import hashlib

class DocumentRepository:

    async def create(self, file: File, content : str) -> Document:
        """
        Create a new document in the database from the file.
        
        :param file: File object containing the file information.
        :return: Document object created from the file.
        """
        hashed_content = hashlib.sha256(content.encode()).hexdigest()
        
        # Create file metadata instead of storing the UploadFile object directly
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