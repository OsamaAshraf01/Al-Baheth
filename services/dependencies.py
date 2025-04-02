from fastapi import HTTPException
from helpers import Settings
from services.Parsing import ParsingService, LangChainService
from services.NLP import LanguageProcessingService, NLTKService
from services.Indexing import IndexingService, PyTerrierService
from models.enums import LanguageProcessingEnum, FileEnum, IndexingEnum


def getParsingService(settings: Settings) -> ParsingService:
    """
    Retrieves the appropriate file service based on the provided settings.

    Args:
        settings (Settings): The settings object containing configuration for the file service.

    Returns:
        FileService: An instance of the selected file service.

    Raises:
        HTTPException: If the specified file service is not found in the settings.
    """
    if settings.PARSING_SERVICE == FileEnum.LangChain.value:
        return LangChainService()
    
    raise HTTPException(
        status_code=404,
        detail="File service not found"
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

    
def getIndexingService(settings: Settings) -> IndexingService:
    """
    Retrieves the appropriate indexing service based on the provided settings.

    Args:
        settings (Settings): The settings object containing configuration for the indexing service.

    Returns:
        IndexingService: An instance of the selected indexing service.

    Raises:
        HTTPException: If the specified indexing service is not found in the settings.
    """
    if settings.INDEXING_SERVICE == IndexingEnum.PyTerrier.value:
        return PyTerrierService()
    
    raise HTTPException(
        status_code=404,
        detail="Indexing service not found"
    )