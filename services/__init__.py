from helpers import Annotated
from fastapi import Depends
from .PDF import PDFReaderService as PDFReaderServiceClass
from .Language import LanguageService as LanguageServiceClass
from  .dependencies import getPDFReaderService, getLanguageService

PDFReaderService = Annotated[PDFReaderServiceClass, Depends(getPDFReaderService)]
LanguageService = Annotated[LanguageServiceClass, Depends(getLanguageService)]