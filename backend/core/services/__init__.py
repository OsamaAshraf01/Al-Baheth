from fastapi import Depends, Request

from .Directory import DirectoryService
from .Indexing import IndexingService as IndexingServiceClass
from .NLP import LanguageProcessingService as LanguageProcessingServiceClass
from .Parsing import ParsingService as ParsingServiceClass
from .dependencies import getParsingService, getLanguageProcessingService, getIndexingService
from ..helpers import Annotated, Settings

ParsingService = Annotated[ParsingServiceClass, Depends(getParsingService)]
LanguageProcessingService = Annotated[LanguageProcessingServiceClass, Depends(getLanguageProcessingService)]


# Modified to include the Request in the dependency chain
def get_indexing_service(settings: Settings, request: Request):
    return getIndexingService(settings, request)


IndexingService = Annotated[IndexingServiceClass, Depends(get_indexing_service)]
