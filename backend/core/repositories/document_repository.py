from models import File, Document
import hashlib

class DocumentRepository:

    async def create(self, file: File, content : str) -> Document:
        """
        Create a new document in the database from the file.
        
        :param file: File object containing the file information.
        :return: Document object created from the file.
        """
        hashed_content = hashlib.sha256(content.encode()).hexdigest()
        document = Document(file=file.file, title=file.file.filename, hashed_content=hashed_content)
        await document.insert()
        return document   