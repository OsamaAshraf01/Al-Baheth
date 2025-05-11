import hashlib
from typing import Optional, Dict, Any

from beanie import PydanticObjectId

from ..models import Document, File
from ..services import IndexingService


class DocumentRepository:

    def __init__(self, indexing_service: IndexingService):
        """
        Initialize the DocumentRepository with an indexing service.
        
        :param indexing_service: An instance of IndexingService for indexing documents.
        """
        self.indexing_service = indexing_service
        self.embedding_model = indexing_service.embedding_model

    async def create(self, file: File, file_title: str, file_content: str) -> Optional[Document]:
        """
        Create a new document in the database from the file.

        :param file: The file object containing the content.
        :param file_title: The title of the file.
        :param file_content: The content of the file to be hashed and embedded.
        :return: Document object created from the file.
        """
        hashed_content = hashlib.sha256(file_content.encode()).hexdigest()

        found = await self.get_by_key(hashed_content)
        if found:
            return None


        document = Document(
            hashed_content=hashed_content,
            parsed_text=file_content,
            embeddings=self.embedding_model.encode(file_content),
            title=file_title,
            bytes_content=await file.read() if file else None,
        )

        await document.insert()

        await self.indexing_service.index(file_id=hashed_content, file_content=file_content)

        return document

    # for testing purposes only
    async def search(self, query: str) -> list:
        """
        Search for documents in the index.
        
        :param query: The cleaned search query.
        :return: A list of document titles matching the search query.
        """
        results = await self.indexing_service.search(query)
        scores = {
            result['file_id']: result['score'] for result in results
        }
        IDs = [result['file_id'] for result in results]
        docs = await Document.find({"hashed_content": {"$in": IDs}}).to_list()
        final_results = [
            {
                "title": doc.title,
                "score": scores[doc.hashed_content],
                "content": doc.parsed_text,
            }
            for doc in docs
        ]

        return final_results

    async def get_by_key(self, hashing_key: str) -> Optional[Document]:
        """
        Get a document by its hashed content.
        
        :param hashing_key: The hashed content of the document.
        :return: Document object if found, None otherwise.
        """
        document = await Document.find_one(Document.hashed_content == hashing_key)
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
