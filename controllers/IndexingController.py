from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
import os
import pyterrier as pt
import requests
from .BaseController import BaseController
from controllers.ProcessingController import ProcessingController
import pandas as pd

class IndexingController(BaseController):
    def __init__(self):
        super().__init__()
        self.index_dir = os.path.join(self.files_dir, "index")
        if not pt.java.started():
            pt.java.init()

    def _get_file_path(self, file_name):
        return os.path.join(self.files_dir, file_name)

    def _preprocess_file(self, file_name: str, controller : ProcessingController = Depends()) -> str:
        """
        Preprocess a file using the /preprocess/{file_name} endpoint.
        
        :param file_name: Name of the file to preprocess.
        :return: Preprocessed text content.
        """
        
        # response = requests.get(f"http://localhost:8000/api/v1/processing/preprocess/{file_name}")
        # if response.status_code != status.HTTP_200_OK:
        #    raise HTTPException(status_code=response.status_code, detail=response.json())
        # return response.json().get("Processed Text", "")
        return controller.preprocess(file_name)

    def _index_files(self, file_names: list):
        """
        Index the preprocessed files using PyTerrier.
        
        :param file_names: List of file names to index.
        """
        indexer = pt.DFIndexer(self.index_dir, overwrite=True)
        docs = []
        for file_name in file_names:
            preprocessed_text = self._preprocess_file(file_name)
            docs.append({
                'docno': file_name,
                'text': preprocessed_text
            })
        docs = pd.DataFrame(docs)
        docs['text'] = docs['text'].astype(str)
        docs['docno'] = docs['docno'].astype(str)
        index_ref = indexer.index(docs['text'], docs['docno'])
        return index_ref

    def index_all_files(self):
        """
        Index all files in the assets folder.
        """
        file_names = [f for f in os.listdir(self.files_dir) if os.path.isfile(os.path.join(self.files_dir, f))]
        if not file_names:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "No files found in the assets folder."}
            )
        
        try:
            index_ref = self._index_files(file_names)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Files indexed successfully.", "index_ref": str(index_ref)}
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))