# ESDSS – Editorial Screening Decision Support System

## Overview

ESDSS (Editorial Screening Decision Support System) is an AI-powered decision support system designed to automate and improve the editorial screening process using an intelligent multi-agent architecture.

## Installation

```bash
# Clone the repository
git clone https://github.com/niklas-silla/esdss.git
cd esdss

# Create and activate environment
conda create -n esdss python=3.12.12 -y
conda activate esdss

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

## Configuration

Create a `.env` file and define the following environment variables:

```bash
LANGSMITH_TRACING=
LANGSMITH_ENDPOINT=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
SEMANTIC_SCHOLAR_API_KEY=
OPENAI_API_KEY= # Only required if OpenAI models are used
```

## Usage

Select the language model in `llm_config.py` (Ollama or OpenAI).

If you want to use **Ollama**, ensure that Ollama is running locally at `http://localhost:11434/` and that the following models are installed:

- `gpt-oss:120b`
- `embeddinggemma:latest`

If you want to use **OpenAI**, provide your API key in the `.env` file:

```bash
OPENAI_API_KEY=sk-...
```

### Starting the application

**Option 1 — Desktop shortcut (recommended for non-technical users)**

Run once to create a desktop icon:

```bash
python create_shortcut.py
```

From then on, double-click **ESDSS** on your Desktop. The server starts in the background and your browser opens automatically.

**Option 2 — Manual start**

```bash
python start.py
```

Or the traditional way:

```bash
uvicorn server:app --port 8000
```

