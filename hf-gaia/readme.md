# hf-gaia

Agent built from the [HF AI Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction), to be evaluated against [General AI Assistants (GAIA)](https://arxiv.org/abs/2311.12983) benchmark.

## GAIA and current score

> GAIA proposes real-world questions that require a set of fundamental abilities such as reasoning, multi-modality handling, web browsing, and generally tool-use proficiency. GAIA questions are conceptually simple for humans yet challenging for most advanced AIs: we show that human respondents obtain 92\% vs. 15\% for GPT-4 equipped with plugins.

The score below is only for Level-1 questions, that are in scope of the course. The questions focus on multi-modality (text, image, audio, video, excel), all kinds of web searches and other tool use, and reasoning.

```sh
Submission result:
{
    "username": "marcinzi",
    "score": 70.0,
    "correct_count": 14,
    "total_attempted": 18,
    "message": "Score calculated successfully: 14/20 total questions answered correctly (18 valid tasks attempted). High score updated on leaderboard.",
    "timestamp": "2025-06-16T09:39:29.321258+00:00"
}
```

## Approach

The approach to the task was testing limits of a single-agent with rich toolkit. 

- **OpenAI 4o** model
- **LangGraph** for control
- **Prompt optimization step**
- **Custom tools**:
  - Wikipedia tool which is searching articles and returning titles with section names. The tool then offers to fetch the requested article sections together with tables content. This controls for pitfalls with wikipedia - large token inputs, lack of tables on non-html API.
  - Excel tool for converting spreadsheets into Pandas dataframes
  - YouTube tool for accessing audio transcriptions, and downolading and breaking videos into key-frames images
  - Google Search and page visit tools

## Usage

### Install dependencies:
```sh
pip install -r requirements.txt
```

You'll need Google Search for developers (100 queries per day are for free),
and a LangFuse account for observability (free hobby tier)

### Configure environment variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY =

GOOGLE_API_KEY = 

LANGFUSE_SECRET_KEY= 
LANGFUSE_PUBLIC_KEY= 
LANGFUSE_HOST= "https://cloud.langfuse.com"
```

### Run

The app is downloading `.data/questions.json` and attachment files locally for faster devloop.
The app is ongoingly updating the questions file with additional attributes: `answer` (tracks agents responses), `correct` (tracks whether the answer was accepted as positive).

Update the `src/app.py` to make a submission.

```sh
usage: app.py [-h] (--task_id TASK_ID | --all | --submit) [--evaluate]                                                                              
Run the agent.

options:
  -h, --help         show this help message and exit
  --task_id TASK_ID  the task id of the question to answer
  --all              all questions
  --submit           submit answers file to responses API
  --evaluate         submit answer to responses API per 1 question and evaluate if answer is correct
```

## Certificate

> [HF Agent Course](https://huggingface.co/learn/agents-course) certifies from 30%

<img src='../docs/Hugging%20Face%20-%20Agents%20Course%20certificate%20-%20Marcin%20Zieminski.webp' alt='HF Agent Course Certificate - Marcin Zieminski' width='300' />
