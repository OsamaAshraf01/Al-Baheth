import os

class DirectoryService:
    # static atribute
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    files_dir = os.path.join(base_dir, "assets")
    index_dir = os.path.join(base_dir, "index")