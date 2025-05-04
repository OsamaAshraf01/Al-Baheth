from fastapi import APIRouter, Depends
from ..helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix='/api/v1',
    tags=["api_v1", "base"]
)

@base_router.get('/')
async def welcome(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    allowed_files = app_settings.FILE_ALLOWED_TYPES
    max_size = app_settings.FILE_MAX_SIZE

    return {
        "app_name": app_name,
        "app_version": "v" + app_version,
        "allowed_types": allowed_files,
        "max_size": str(max_size) + "Mb"
    }
