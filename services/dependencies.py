from fastapi import HTTPException
from helpers import Settings
from services.PDF import PDFReaderService, PyPDF2ReaderService
from services.Language import LanguageProcessingService, NLTKService
from services.File import FileService, LongChainService
from models.enums import PDFEnum, LanguageProcessingEnum, FileEnum


def getPDFReaderService(settings: Settings) -> PDFReaderService:
    """
    Get the PDF reader service based on the service name.
    
    :return: Instance of the PDF reader service based on .env file.
    """
    if settings.PDF_READER == PDFEnum.PyPDF2.value:
        return PyPDF2ReaderService()
    
    raise HTTPException(
        status_code=404,
        detail="PDF Reader service not found"
    )
    
def getLanguageProcessingService(settings: Settings) -> LanguageProcessingService:
    """
    Retrieves the appropriate language processing service based on the provided settings.

    Args:
        settings (Settings): The configuration settings that determine which language processing service to use.

    Returns:
        LanguageProcessingService: An instance of the selected language processing service.

    Raises:
        HTTPException: If the specified language processor is not found in the settings.
    """
    if settings.LANGUAGE_PROCESSOR == LanguageProcessingEnum.NLTK.value:
        return NLTKService()
    
    raise HTTPException(
        status_code=404,
        detail="Language processor service not found"
    )
    
def getFileService(settings: Settings) -> FileService:
    """
    Retrieves the appropriate file service based on the provided settings.

    Args:
        settings (Settings): The settings object containing configuration for the file service.

    Returns:
        FileService: An instance of the selected file service.

    Raises:
        HTTPException: If the specified file service is not found in the settings.
    """
    if settings.FILE_SERVICE == FileEnum.LongChain.value:
        return LongChainService()
    
    raise HTTPException(
        status_code=404,
        detail="File service not found"
    )