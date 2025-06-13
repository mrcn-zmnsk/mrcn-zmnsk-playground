# hf-gaia

Agent built from the HF Agent Course, to be evaluated against [General AI Assistants (GAIA)](https://arxiv.org/abs/2311.12983) benchmark L1.

## Current score

```sh
Submission result:
{
    "username": "marcinzi",
    "score": 45.0,
    "correct_count": 9,
    "total_attempted": 17,
    "message": "Score calculated successfully: 9/20 total questions answered correctly (17 valid tasks attempted). High score updated on leaderboard.",
    "timestamp": "2025-06-13T13:26:42.739334+00:00"
}
```

> [HF Agent Course](https://huggingface.co/learn/agents-course) certifies from 30%

<img src='../docs/Hugging%20Face%20-%20Agents%20Course%20certificate%20-%20Marcin%20Zieminski.webp' alt='HF Agent Course Certificate - Marcin Zieminski' width='400' />

## Features

- **OpenAI 4o** model
- **LangGraph** for control
- **Prompt optimization step**
- **Multi-modal** works with images, audio, excel (video coming)
- **Custom tools**: Wikipedia (spent too much time here, parsing page contents and scraping tables)

## Usage

### Install dependencies:
```sh
pip install -r requirements.txt
```

## Configure environment variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY =
SERPAPI_API_KEY = 

LANGFUSE_SECRET_KEY= 
LANGFUSE_PUBLIC_KEY= 
LANGFUSE_HOST= "https://cloud.langfuse.com"
```

## Run

The app is downloading `.data/questions.json` and attachment files locally for faster devloop.
The app is ongoingly updating `.data/answers.json` so that you can work with questions 1 by 1.

Update the `src/app.py` to make a submission.

```sh
python src/gaia_agent.py --task_id "8e867cd7-cff9-4e6c-867a-ff5ddc2550be"
```