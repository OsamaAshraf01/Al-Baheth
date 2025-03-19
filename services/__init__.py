from typing_extensions import Annotated
from .PDF import PDFReaderService as PDFReaderServiceClass
from .Language import LanguageService as LanguageServiceClass
from  .dependencies import getPDFReaderService, getLanguageService

PDFReaderService = Annotated[PDFReaderServiceClass, getPDFReaderService]
LanguageService = Annotated[LanguageServiceClass, getLanguageService]