from helpers.config import get_settings
import os

# this controller will contain the common methods that will be used by other controllers
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))  # To get the dir of src folder
        self.files_dir = os.path.join(self.base_dir, "assets")