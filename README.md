# Diet Planning Chatbot

A Gradio-based diet planning assistant that creates personalised meal plans through a streaming chat interface. The chatbot uses LangChain, stores conversation history in SQLite, and loads its system instructions from `prompt.md`.

## Features

- Streaming chatbot responses
- Gradio web interface
- Persistent conversation history using SQLite
- Session selection for previous conversations
- Diet-planning system prompt with safety and nutritional guidance
- Environment-variable based API key management

## Project Structure

```text
.
├── main.py              # Application entry point
├── logic.py             # Chatbot logic, model setup, session history
├── ui.py                # Gradio interface
├── prompt.md            # System prompt for the diet assistant
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variable file
├── .gitignore           # Files Git should ignore
└── README.md            # Project documentation
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your local `.env` file

Copy the example file:

```bash
cp .env.example .env
```

Then edit `.env` and add your real API key:

```env
OPENAI_API_KEY=your_real_api_key_here
```

Do **not** upload your real `.env` file to GitHub. The `.gitignore` file already excludes it.

## Run the app

```bash
python main.py
```

Gradio will start a local web app and provide a browser link.

## Notes on API Keys

This project uses `python-dotenv` to load environment variables from `.env`. Your actual API key should only live on your local machine or in deployment secrets, such as Hugging Face Spaces Secrets, GitHub Actions Secrets, or another secure environment variable manager.

## Deployment Notes

For Hugging Face Spaces or similar platforms, do not upload `.env`. Instead, add `OPENAI_API_KEY` through the platform's secret/environment variable settings.

## Important Health Disclaimer

This chatbot provides general diet-planning guidance only. It should not replace advice from a doctor, registered dietitian, or qualified healthcare professional, especially for users with medical conditions, eating disorders, pregnancy, allergies, or specialist nutritional requirements.
