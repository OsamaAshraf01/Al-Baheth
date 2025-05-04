import os

import pyterrier as pt

from .IndexingService import IndexingService
from ...services.Directory import DirectoryService


class PyTerrierService(IndexingService):

    def __init__(self):
        super().__init__()
        # if not pt.java.started():
        #     pt.init()  --> deprecated since pyterrier 0.11.0.
        self.indexer = pt.IterDictIndexer(
            DirectoryService.index_dir,
            meta={'docno': 200},
            termpipelines=[],  # to disable default term pipelines (Stopwords and PorterStemmer)
        )

    def isExistingIndex(self) -> bool:
        """
        Check if the index already exists at the specified path.
        
        :return: True if the index exists, False otherwise.
        """
        return os.path.exists(os.path.join(DirectoryService.index_dir, "data.properties"))

    # def index(self, corpus: dict) -> str:
    #     # return self.indexer.index(corpus, append=True) if self.isExistingIndex() else self.indexer.index(corpus)
    #     return self.indexer.index(corpus)

    async def index(self, file_id: str, content: str) -> bool:
        """
        Index the given corpus and return the index reference.
        
        :param corpus: Dictionary containing the corpus to index. It consists of two keys: docno and text.
        :return: Index reference.
        """
        pass
