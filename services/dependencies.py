from fastapi import Depends, HTTPException
from helpers.config import get_settings, Settings
from services.PDF import PDFReaderService, PyPDF2ReaderService
from services.Language import LanguageService, NLTKService

def getPDFReaderService(settings: Settings = Depends(get_settings)) -> PDFReaderService:
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
    
def getLanguageService(settings: Settings = Depends(get_settings)) -> LanguageService:
    if settings.LANGUAGE_PROCESSOR == "NLTK":
        return NLTKService()
    
    raise HTTPException(
        status_code=404,
        detail="Language processor service not found"
    )