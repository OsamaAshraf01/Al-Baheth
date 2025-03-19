from fastapi import HTTPException
from helpers import Settings
from services.PDF import PDFReaderService, PyPDF2ReaderService
from services.Language import LanguageProcessingService, NLTKService
from models.enums import PDFEnum, LanguageProcessingEnum

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