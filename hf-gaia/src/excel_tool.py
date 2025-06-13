from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
import pandas as pd

class ExcelToolInput(BaseModel):
    file_name: str = Field(..., description="The file name of the Excel file to process.")

class ExcelTool(BaseTool):

    name: str = "Excel_tool"
    description: str = "A tool for loading Excel files."
    args_schema: Type[BaseModel] = ExcelToolInput
   

    def _run(self, file_name: str) -> str:
        df = pd.read_excel(f'./data/{file_name}', engine='openpyxl')
        result = df.to_markdown(index=False, tablefmt="grid")
        return result


