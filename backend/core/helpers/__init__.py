from fastapi import Depends
from typing_extensions import Annotated
from .config import Settings as SettingsClass, get_settings
from .Lifespan import lifespan

Settings = Annotated[SettingsClass, Depends(get_settings)]