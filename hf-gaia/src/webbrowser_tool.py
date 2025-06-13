from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
from markdownify import markdownify as md
import requests

class WebBrowserToolInput(BaseModel):
    url: str = Field(..., description="The url of the page to visit")

class WebBrowserTool(BaseTool):

    name: str = "webbrowser_tool"
    description: str = "A tool for visiting web pages for information. Returns markdown version of them"
    args_schema: Type[BaseModel] = WebBrowserToolInput
    
    def _run(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        
        md_content = md(response.text)

        return md_content.strip()
        


