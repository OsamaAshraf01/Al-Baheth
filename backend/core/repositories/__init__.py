from fastapi import Depends
from typing_extensions import Annotated

from .document_repository import DocumentRepository

DocumentRepo = Annotated[DocumentRepository, Depends(DocumentRepository)]
