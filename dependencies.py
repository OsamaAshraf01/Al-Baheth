from fastapi import Depends, HTTPException
import services
from services.PDF import PDFReaderService
from helpers.config import get_settings, Settings
import services.PDF.PyPDF2ReaderService

def getPDFReaderService(settings: Settings = Depends(get_settings)) -> PDFReaderService:
    """
    Get the PDF reader service based on the service name.
    
    :return: Instance of the PDF reader service based on .env file.
    """
    if settings.PDF_READER == "PyPDF2":
        return services.PyPDF2.PyPDF2ReaderService()
    
    raise HTTPException(
        status_code=404,
        detail="PDF Reader service not found"
    )