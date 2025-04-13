from helpers import Annotated
from fastapi import Depends
from .Parsing import ParsingService as ParsingServiceClass
from .NLP import LanguageProcessingService as LanguageProcessingServiceClass
from .Indexing import IndexingService as IndexingServiceClass
from .dependencies import getParsingService, getLanguageProcessingService, getIndexingService
from .Directory import DirectoryService

ParsingService = Annotated[ParsingServiceClass, Depends(getParsingService)]
LanguageProcessingService = Annotated[LanguageProcessingServiceClass, Depends(getLanguageProcessingService)]
IndexingService = Annotated[IndexingServiceClass, Depends(getIndexingService)]
