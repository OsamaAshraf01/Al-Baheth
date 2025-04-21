from .document_repository import DocumentRepository
from typing_extensions import Annotated
from fastapi import Depends

DocumentRepo = Annotated[DocumentRepository, Depends(DocumentRepository)]