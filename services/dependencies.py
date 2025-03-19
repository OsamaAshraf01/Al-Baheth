from fastapi import HTTPException
from helpers import Settings
from services.PDF import PDFReaderService, PyPDF2ReaderService
from services.Language import LanguageProcessingService, NLTKService

def getPDFReaderService(settings: Settings) -> PDFReaderService:
    """
    Get the PDF reader service based on the service name.
    
    :return: Instance of the PDF reader service based on .env file.
    """
    if settings.PDF_READER == "PyPDF2":
        return PyPDF2ReaderService()
    
    raise HTTPException(
        status_code=404,
        detail="PDF Reader service not found"
    )
    
def getLanguageProcessingService(settings: Settings) -> LanguageProcessingService:
    if settings.LANGUAGE_PROCESSOR == "NLTK":
        return NLTKService()
    
    raise HTTPException(
        status_code=404,
        detail="Language processor service not found"
    )