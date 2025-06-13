import requests, os, json

DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"

os.makedirs('./data', exist_ok=True)

def get_questions():
    """Fetch questions from the API."""
    
    questions_file = './data/questions.json'

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



def update_answer(task_id, answer):

    answers_file = './data/answers.json'
    data = {
        "task_id": task_id,
        "submitted_answer": answer
    }
    
    if os.path.exists(answers_file):
        with open(answers_file, 'r') as f:
            submission_json = json.load(f)
    else:
        submission_json = {
            "username": "marcinzi", 
            #"agent_code": agent_code, 
            "answers": []
        }

    filtered = [a for a in submission_json['answers'] if a['task_id'] != task_id]
    filtered.append(data)
    submission_json['answers'] = filtered
    
    with open(answers_file, 'w') as f:
        json.dump(submission_json, f, indent=4) 

    return submission_json

def submit_answers():
    submit_url = f"{DEFAULT_API_URL}/submit"
    answers_file = './data/answers.json'
    
    with open(answers_file, 'r') as f:
        submission_json = json.load(f)

    response = requests.post(submit_url, json=submission_json, timeout=15)
    response.raise_for_status()
    
    result = response.json()
    
    print('Submission result:')
    print(json.dumps(result, indent=4))
    
    return result