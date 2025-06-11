import dotenv, argparse
from langchain_core.messages import HumanMessage
from langfuse.langchain import CallbackHandler
from agent_graph import build_agent_graph

dotenv.load_dotenv()

def main(prompt: str):
    agent = build_agent_graph()

    print(f'Executing agent for prompt: {prompt}')
    langfuse_handler = CallbackHandler()
    for chunk in agent.stream(
        {
            "messages": [
                HumanMessage(content=prompt),
            ]
        }, 
        config={"callbacks": [langfuse_handler]},
        stream_mode='updates'
    ):
        for val in chunk.values():
            for m in val['messages']:
                m.pretty_print()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the agent.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="I am going on a trip to France. We're considering to visit a museum. Can you recommend something?",
        help="Prompt for the agent"
    )
    args = parser.parse_args()

    main(args.prompt)