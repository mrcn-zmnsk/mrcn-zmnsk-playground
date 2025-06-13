from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
from langchain_community.utilities import SerpAPIWrapper
import dotenv

class WebSearchToolInput(BaseModel):
    query: str = Field(..., description="The query to search the web.")

class WebSearchTool(BaseTool):

    name: str = "websearch_tool"
    description: str = "A tool for browsing the web for information."
    args_schema: Type[BaseModel] = WebSearchToolInput
    
    dotenv.load_dotenv()
    serpSearch: SerpAPIWrapper = SerpAPIWrapper()

    def _run(self, query: str) -> str:
        answer =  self.serpSearch.run(query)
        return answer
        


