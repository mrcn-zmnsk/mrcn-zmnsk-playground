import asyncio, argparse
from llama_index.core.agent.workflow import AgentWorkflow, AgentStream
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec

llm = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-Coder-32B-Instruct")

agent = AgentWorkflow.from_tools_or_functions(    
    system_prompt="A helpful assistant that can use a tool to query the web.",
    tools_or_functions=DuckDuckGoSearchToolSpec().to_tool_list(), 
    llm=llm,
)


async def main(user_prompt):
    
    handler = agent.run(user_msg=user_prompt)

    async for ev in handler.stream_events():
        if isinstance(ev, AgentStream):
            print(ev.delta, end="", flush=True)

    print(await handler)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the multi-agent system.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="What is the population of Helsinge, Denmark?",
        help="Prompt for the manager agent"
    )
    args = parser.parse_args()

    asyncio.run(main(args.prompt))

