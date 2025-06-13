from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
import wikipedia
from wikipediaapi import Wikipedia, ExtractFormat, WikipediaPageSection
from wikitables import import_tables
import markdownify as md
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

class WikipediaSearchToolInput(BaseModel):
    query: str = Field(..., description="The query for wikipedia search")


class WikipediaSearchTool(BaseTool):

    name: str = "WikipediaSearch_tool"
    description: str = "A tool querying wikipedia. Returns a list of page titles matching the query."
    args_schema: Type[BaseModel] = WikipediaSearchToolInput
    
    def _run(self, query: str) -> list[str]:
        search, suggestion = wikipedia.search(query, results=10, suggestion=True)

        if suggestion:
            return [suggestion]
        elif len(search) > 0:
            return search
        else:
            return []


class WikipediaPageToolInput(BaseModel):
    page_title: str = Field(..., description="The page title to retrieve from wikipedia")
    page_sections: list[str] = Field(..., description="Explicit list of sections to retrieve from the page. If empty, the result will only list available section names, for you to read and explicity use in subsequent call")

class WikipediaPageTool(BaseTool):

    name: str = "WikipediaPage_tool"
    description: str = "A tool for loading full wikipedia page by title."
    args_schema: Type[BaseModel] = WikipediaPageToolInput

    wikipedia_api: Wikipedia = Wikipedia(
        user_agent='GAIA evaluation agent (marcin.zieminski@gmail.com)',
        language='en',
        extract_format=ExtractFormat.WIKI,
    )
    
    def get_tables(self, page_title: str, page_sections: list[str]) -> list[str]:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "parse",
            "page": page_title,
            "prop": "text",
            "format": "json",
        }

        res = requests.get(url, params=params)
        html = res.json()["parse"]["text"]["*"]

        result = {}

        soup = BeautifulSoup(html, 'html.parser')
        for section in soup.find_all(['h2', 'h3']):
            section_name = section.get_text()
            if section_name in page_sections:    
                for table in section.find_all_next('table', class_='wikitable'):
                    
                    # Ugly fix for Wikipedia table with a html tag:  <td colspan="2;"/> breaking pandas.read_html
                    for td in table.find_all('td'):
                        colspan = td.get('colspan')
                        if colspan and not colspan.isdigit():
                            td['colspan'] = ''.join(filter(str.isdigit, colspan))

                    dfs = pd.read_html(StringIO(str(table)), flavor='html5lib')
                    for df in dfs:
                        if section_name in result:
                            result[section_name].append(df)
                        else:
                            result[section_name] = [df]
                        
        return result

    def _run(self, page_title: str, page_sections: list[str] = []) -> str:
        try:        
            wikipage = self.wikipedia_api.page(page_title.strip(), unquote=True)
            
            result = f"Wikipedia page: {wikipage.title}\n\n"

            if len(page_sections) == 0: 
                result += "Available sections:\n"
                result += self.print_sections('', wikipage.sections)
            else:
                tables = self.get_tables(page_title, page_sections)

                for s in page_sections:
                    curated = s.replace('#','').strip()
                    for ss in wikipage.sections_by_title(curated):
                        result += f"{'#' * ss.level} {ss.title}\n"
                        result += f"{ss.text}\n"
                        for t in tables.get(ss.title, []):
                            result += f'\n\n{t.to_markdown(index=False, tablefmt="grid")}'

            return result
        except Exception as e:
            return f"Page: {page_title} does not exist or is not accessible. {e}"
        
    def print_sections(self, result:str, sections: list[WikipediaPageSection]) -> str:
        for s in sections:
            result += f"{'#' * s.level} {s.title}\n"
            result = self.print_sections(result, s.sections)
        return result



#tool = WikipediaPageTool()
#result = tool._run('1928 Summer Olympics', ['Venues', 'Participating nations'])
#print(result)