from smolagents import CodeAgent, ToolCallingAgent, VisitWebpageTool, GoogleSearchTool, InferenceClientModel
import dotenv, argparse

dotenv.load_dotenv()

coding_model = InferenceClientModel(
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct'
)

reasoning_model = InferenceClientModel(
    model_id='meta-llama/Llama-3.3-70B-Instruct',
    temperature=0.0,
    max_tokens=8182,
)

web_agent = CodeAgent(
    model = coding_model,
    tools=[GoogleSearchTool(provider='serpapi'), VisitWebpageTool()],
    max_steps=5,
    name='WebAgent',
    description='An agent that can search the web and visit webpages to gather information.',
)
   
manager_agent = CodeAgent(
    model=reasoning_model,
    tools=[],
    max_steps=5,
    managed_agents=[web_agent],  # The web_agent will be managed by the manager_agent
    name='ManagerAgent',
    planning_interval=3
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the multi-agent system.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="What is the population of Helsinge, Denmark?",
        help="Prompt for the manager agent"
    )
    args = parser.parse_args()

    prompt = args.prompt
    response = manager_agent.run(prompt)
    
else:
    prompt = 'What is the population of Helsinge, Denmark?'
    response = manager_agent.run(prompt)

print("Response:", response)