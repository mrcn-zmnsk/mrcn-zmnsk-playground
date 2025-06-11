from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI
from retriever_tool import RetrieverTool
from websearch_tool import WebSearchTool

def build_agent_graph():

    # LLM
    tools = [
        RetrieverTool(),
        WebSearchTool()
    ]
    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
    chat_with_tools = llm.bind_tools(tools)

    # State
    class AgentState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]

    # Assistant node
    def assistant(state: AgentState):
        return {
            "messages": [chat_with_tools.invoke(state["messages"])],
        }

    ## Graph
    builder = StateGraph(AgentState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    
    agent_graph = builder.compile()
    return agent_graph