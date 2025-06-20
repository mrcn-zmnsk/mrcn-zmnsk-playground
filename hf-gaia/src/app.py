import dotenv, argparse
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse.langchain import CallbackHandler
from agent_graph import build_agent_graph
import hf_facade

dotenv.load_dotenv()

def answer_question(question):
    try:
        if 'disabled' in question and question['disabled'] == True:
            print(f'\n\nSkipping disabled question {question["task_id"]} : {question["question"]}')
            return None
        else:
            print(f'\n\nExecuting agent for question: {question['task_id']}\n{question['question']}\n{"=" * 50}')
        
        agent = build_agent_graph()
        
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
    except Exception as e:
        print(f'Error while answering question {question["task_id"]}: {e}')
        return None


# Unsolved questions:
# science papers / browser: 840bfca7-4f7b-481a-8794-c560c340185d, bda648d7-d618-4883-88f4-3466eabd860e
# video processing: a1e91b78-d3d8-4675-bb8d-62741b4b68a6

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the agent.")

    group = parser.add_mutually_exclusive_group(required=True)    
    
    group.add_argument(
        "--task_id",
        type=str,
        help="the task id of the question to answer"
    )

    group.add_argument(
        "--all",
        action='store_true',
        help="all questions"
    )

    group.add_argument(
        "--submit",
        action='store_true',
        help="submit answers file to responses API"
    )

    parser.add_argument(
        "--evaluate",
        action='store_true',
        help="evaluate questions 1 by 1"
    )
    args = parser.parse_args()

    questions = []

    if args.submit:
        hf_facade.evaluate_all_answers()
        exit(0)

    if args.task_id:
        questions = [hf_facade.get_question(args.task_id)]  
    elif args.all:
        questions = hf_facade.get_questions()

    for q in questions:
        if not q.get('disabled', False) and not q.get('answer', None):
            answer = answer_question(q)
            
            correct = None
            if answer != None and args.evaluate:
                correct = hf_facade.evaluate_answer(q['task_id'], answer)
                print(f'=== Answer: {answer} for question {q["task_id"]} is {'CORRECT' if correct else 'INCORRECT'}')

            if answer != None:
                q["answer"] = answer

            if correct != None:
                q["correct"] = correct

            hf_facade.update_question(q)        

