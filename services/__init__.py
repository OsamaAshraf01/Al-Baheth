from helpers import Annotated
from fastapi import Depends
from .PDF import PDFReaderService as PDFReaderServiceClass
from .Language import LanguageProcessingService as LanguageProcessingServiceClass
from .File import FileService as FileServiceClass
from  .dependencies import getPDFReaderService, getLanguageProcessingService, getFileService
from .Directory import DirectoryService

PDFReaderService = Annotated[PDFReaderServiceClass, Depends(getPDFReaderService)]
LanguageProcessingService = Annotated[LanguageProcessingServiceClass, Depends(getLanguageProcessingService)]
FileService = Annotated[FileServiceClass, Depends(getFileService)]