from controllers import BaseController

class QueryController(BaseController):
    async def query(self, query):
        return {"query": query}