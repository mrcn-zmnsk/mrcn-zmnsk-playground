import requests, os, json

DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"

template_submission_json = {
    "username": "marcinzi", 
    "agent_code": "https://huggingface.co/spaces/marcinzi/Final_Assignment_marcinzi/tree/main",
    "answers": []
}

os.makedirs('./data', exist_ok=True)
questions_file = './data/questions.json'

def get_questions():
    """Fetch questions from the API."""
    
    if os.path.exists(questions_file):
        print(f'Fetching questions from file {questions_file} ...')
        with open(questions_file, 'r') as f:
            questions_data = json.load(f)        
    else:        
        print('Fetching questions from the API...')
        questions_url = f"{DEFAULT_API_URL}/questions"
        response = requests.get(questions_url, timeout=15)
        response.raise_for_status()
        questions_data = response.json()

        with open('./data/questions.json', 'w') as f:            
            json.dump(questions_data, f, indent=4)

    #print('Questions fetched:')
    for q in questions_data:
        #print_question(q)
        download(q)

    return questions_data

def get_question(task_id: str):
    questions = get_questions()  # Fetch and print all questions
    q = next(item for item in questions if item['task_id'] == task_id)
    return q

def get_random_question():
    """Fetch a random question from the API."""
    random_question_url = f"{DEFAULT_API_URL}/random-question"
    response = requests.get(random_question_url, timeout=15)
    response.raise_for_status()
    question = response.json()
    
    print('Random question fetched:')
    print_question(question)

    download(question)
    
    return question

def download(question):
    """Download the task data from the API."""

    file_name = question['file_name']

    if file_name:
        file_path = f'./data/{file_name}'
        
        if os.path.exists(file_path) == False:
            download_url = f"{DEFAULT_API_URL}/files/{question['task_id']}"
            response = requests.get(download_url, timeout=15)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)

            print(f'Downloaded file: {file_name}')
    

def print_question(q):
    """Print the question in a formatted way."""
    print('=' * 40)
    print(f'Task id: {q["task_id"]}')
    print(f'Question: {q["question"]}')


def evaluate_answer(task_id, answer):
    data = {
        "task_id": task_id,
        "submitted_answer": answer,
    }
    
    response = submit_answers([data])

    return response['correct_count'] > 0

def evaluate_all_answers():
    with open(questions_file, 'r') as f:
        questions_json = json.load(f)

    data = [
        { 
            "task_id": a['task_id'], 
            'submitted_answer': a['answer']
        } for a in questions_json if 'answer' in a
    ]
    
    return submit_answers(data)


def update_question(question):
    with open(questions_file, 'r') as f:
        questions_json = json.load(f)

    index = next((i for i, q in enumerate(questions_json) if q['task_id'] == question['task_id']), None)
    if index != None:
        questions_json[index] = question
        
    with open(questions_file, 'w') as f:
        json.dump(questions_json, f, indent=4) 


def submit_answers(answers):
    submit_url = f"{DEFAULT_API_URL}/submit"

    submission_json = template_submission_json.copy()    
    submission_json['answers'] = answers

    response = requests.post(submit_url, json=submission_json, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    
    print('Submission result:')
    print(json.dumps(result, indent=4))
    
    return result