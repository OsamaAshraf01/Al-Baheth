from fastapi import Depends
from typing_extensions import Annotated
from .custom_assertions import AssertExistence
from .decorators import execution_manager
from .config import Settings as SettingsClass, get_settings

Settings = Annotated[SettingsClass, Depends(get_settings)]