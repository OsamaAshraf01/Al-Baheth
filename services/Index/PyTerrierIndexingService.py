from .IndexingService import IndexingService
from services import DirectoryService
import pyterrier as pt
import os

class PyTerrierIndexingService(IndexingService):
    
    def __init__(self):
        super().__init__()
        if not pt.java.started():
            pt.init()
        self.indexer = pt.IterDictIndexer(DirectoryService.index_dir)
    
    def isExistingIndex(self) -> bool:
        """
        Check if the index already exists at the specified path.
        
        :return: True if the index exists, False otherwise.
        """
        return os.path.exists(os.path.join(DirectoryService.index_dir, "data.properties"))
            
    def index(self, corpus: dict) -> str:
        return self.indexer.index(corpus, append=self.isExistingIndex())