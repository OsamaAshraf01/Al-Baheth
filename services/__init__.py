from helpers import Annotated
from fastapi import Depends
from .PDF import PDFReaderService as PDFReaderServiceClass
from .Language import LanguageProcessingService as LanguageProcessingServiceClass
from  .dependencies import getPDFReaderService, getLanguageProcessingService
from .Directory import DirectoryService

PDFReaderService = Annotated[PDFReaderServiceClass, Depends(getPDFReaderService)]
LanguageProcessingService = Annotated[LanguageProcessingServiceClass, Depends(getLanguageProcessingService)]