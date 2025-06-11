from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
from langchain_chroma import Chroma
from vector_store import get_vector_store

class RetrieverToolInput(BaseModel):
    query: str = Field(..., description="The query to search for locations.")


class RetrieverTool(BaseTool):

    name: str = "tripadvisor_tool"
    description: str = "A tool for retrieving information about locations, such as names, categories, ratings and URLs, from TripAdvisor"
    args_schema: Type[BaseModel] = RetrieverToolInput

    vector_store: Chroma = get_vector_store()

    def _run(self, query: str) -> str:
        results = self.vector_store.similarity_search(query, k=5)
        if results:
            return "\n\n".join([doc.page_content for doc in results])
        else:
            return "No matching guest information found."

    