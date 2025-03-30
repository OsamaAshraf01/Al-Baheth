import os

class DirectoryService:
    # class atributes
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    files_dir = os.path.join(base_dir, "assets")
    index_dir = os.path.join(base_dir, "index")
    
    @classmethod
    def get_file_path(cls, file_name):
        return os.path.join(cls.files_dir, file_name)