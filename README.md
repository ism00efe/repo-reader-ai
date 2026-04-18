# RepoReader AI

Built for the MLH AI Hackfest 2026 (Category: Best Use of Gemini API).

I built this because reading massive, undocumented codebases to figure out what a project does or if it has basic security flaws takes too much time. 

RepoReader AI takes a public GitHub URL, fetches the core files, and uses Gemini 2.5 Flash to generate:
1. A quick summary of the tech stack.
2. Security red flags (like running docker as root, outdated dependencies, etc.)
3. A live Mermaid.js architecture diagram.

## Tech Stack
- FastAPI for the backend.
- Streamlit for the UI.
- Google Gemini 2.5 Flash (via `google-generativeai`).

## The Prompt Engineering Issue
Getting an LLM to output valid Mermaid.js inside a JSON schema without breaking the Streamlit UI was the hardest part. Standard newlines or markdown backticks kept crashing the JSON parser. 

To fix this, I used strict prompt engineering:
- Forced `response_mime_type: application/json`
- Instructed Gemini to use semicolons (`;`) instead of newlines for the graphs.
- Enforced strict alphanumeric Node IDs to make the rendering stable.

## How to run locally

1. Clone the repo:
git clone https://github.com/your-username/repo-reader-ai.git
cd repo-reader-ai

2. Setup virtual environment:
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

3. Add your Gemini API key in a `.env` file:
GEMINI_API_KEY=your_api_key_here

4. Run the backend (Terminal 1):
uvicorn main:app --reload

5. Run the frontend (Terminal 2):
streamlit run frontend.py
