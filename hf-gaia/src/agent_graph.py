from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_experimental.tools.python.tool import PythonAstREPLTool as PythonExecutor
from langchain_openai import ChatOpenAI
from websearch_tool import WebSearchTool
from webbrowser_tool import WebBrowserTool
from wikipediasearch_tool import WikipediaSearchTool, WikipediaPageTool
from audiotranscribe_tool import AudioTranscribeTool
from excel_tool import ExcelTool


def get_image_base64(file_name):
    import base64
    with open(f'./data/{file_name}', "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def build_agent_graph():
    # Tools
    tools = [
        WebSearchTool(),
        WebBrowserTool(),
        WikipediaSearchTool(),
        WikipediaPageTool(),
        AudioTranscribeTool(),
        PythonExecutor(),
        ExcelTool()
    ]
    
    # LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
    chat_with_tools = llm.bind_tools(tools)
    
    # Graph
    ## State
    class AgentState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]
        file_name: str | None

    ## Assistant node
    def improve_prompt(state: AgentState):
        user_prompt = state["messages"][-1]
        new_prompt = chat_with_tools.invoke([
            HumanMessage(content=f"Improve the prompt for clarity and effectiveness. Return only the new prompt. Original prompt: {user_prompt.content}")
        ]).content

        user_prompt.content = new_prompt

        if state['file_name']:
            user_prompt.content = user_prompt.content.replace('Strawberry pie.mp3', state['file_name']).replace('Homework.mp3', state['file_name'])

            extension = state['file_name'].split('.')[-1]

            match extension:
                case 'png':
                    image_base64 = get_image_base64(state['file_name'])
                    user_prompt.content.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    )   
                case 'py':
                    with open(f'./data/{state["file_name"]}', 'r') as f:
                        script = f"'''py\n{f.read()}\n'''"

                    state["messages"].append(
                        HumanMessage(content=f"Here is the script:\n{script}")
                    )   
                case 'xlsx':
                    state["messages"].append(
                        HumanMessage(content=f"The Excel file path: {state['file_name']}")
                    )                                   

        return state
    
    def assistant(state: AgentState):
        return {
            "messages": [chat_with_tools.invoke(state["messages"])],
        }
    
    builder = StateGraph(AgentState)

    builder.add_node("improve_prompt", improve_prompt)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.set_entry_point("improve_prompt")
    builder.add_edge("improve_prompt", "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    
    agent_graph = builder.compile()
    return agent_graph