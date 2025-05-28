import os, pytest, sys
from tools import *

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5
    assert multiply(0, 100) == 0

def test_visit_webpage_tool():
    tool = VisitWebpageTool()
    # Test with a valid URL
    url = "https://www.example.com"
    result = tool.forward(url)
    assert isinstance(result, str)  # Should return a markdown string
    assert "This domain is for use in illustrative examples in documents." in result

def test_websearch_tool():
    tool = WebSearchTool()
    # Test with a valid query
    query = "Python programming"
    result = tool.forward(query)
    assert isinstance(result, str)  # Should return a search result string
    assert "Python programming" in result
