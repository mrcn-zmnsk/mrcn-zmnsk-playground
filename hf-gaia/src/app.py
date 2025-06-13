import dotenv, argparse
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse.langchain import CallbackHandler
from agent_graph import build_agent_graph
import hf_facade

dotenv.load_dotenv()

def answer_question(question):
    agent = build_agent_graph()

    print(f'Executing agent for question: {question['task_id']}\n{question['question']}\n{"=" * 50}')
    
    system_prompt = """You are a general AI assistant. I will ask you a question. 
Report your thoughts, and finish your answer with the following template: FINAL ANSWER: [YOUR FINAL ANSWER]. 
YOUR FINAL ANSWER should be a number OR as few words as possible OR a comma separated list of numbers and/or strings. 
If you are asked for a number, don't use comma to write your number neither use units such as $ or percent sign unless specified otherwise. 
If you are asked for a string, don't use articles, neither abbreviations (e.g. for cities), and write the digits in plain text unless specified otherwise. 
If you are asked for a comma separated list, apply the above rules depending of whether the element to be put in the list is a number or a string."""

    user_prompt = [
        question['question']
    ]

    starting_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    final_answer = None

    langfuse_handler = CallbackHandler()
    for chunk in agent.stream(
        {            
            "messages": starting_messages,
            "file_name": question['file_name'],
        }, 
        config={"callbacks": [langfuse_handler]},
        stream_mode='updates'
    ):
        for val in chunk.values():
            for m in val['messages']:
                m.pretty_print()
                if m.type == 'ai' and 'FINAL ANSWER:' in m.content:
                    final_answer = m.content.split('FINAL ANSWER:')[1].strip()

    return final_answer


# Unsolved questions:
# science papers / browser: 840bfca7-4f7b-481a-8794-c560c340185d, bda648d7-d618-4883-88f4-3466eabd860e
# video processing: 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the agent.")
    parser.add_argument(
        "--task_id",
        type=str,
        default="cf106601-ab4f-4af9-b045-5295fe67b37d",
        help="Prompt for the agent"
    )
    args = parser.parse_args()

    q = hf_facade.get_question(args.task_id)  
    answer = answer_question(q)
    update_answer = hf_facade.update_answer(args.task_id, answer)
    print(f"\n\n{'=' *10} FINAL ANSWER = {answer} {'=' *10}")
    

#hf_facade.submit_answers()

