from fastapi import Depends
from typing_extensions import Annotated

from .Lifespan import lifespan
from .config import Settings as SettingsClass, get_settings

Settings = Annotated[SettingsClass, Depends(get_settings)]
