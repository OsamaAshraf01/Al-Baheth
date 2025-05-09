from fastapi import Depends

from ..controllers import BaseController, DataController
from ..repositories import DocumentRepo


class QueryController(BaseController):
    def __init__(
            self,
            document_repository: DocumentRepo,
            data_controller: DataController = Depends()
    ):
        super().__init__()
        self.data_controller = data_controller
        self.document_repository = document_repository

    async def query(self, query: str) -> list:
        """
        Search for documents in the index.

        :param query: The search query.
        :return: A list of document titles matching the search query.
        """
        query = self.data_controller.clean_text(query)
        return await self.document_repository.search(query)
