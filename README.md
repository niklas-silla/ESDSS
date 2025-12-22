# ESDSS – Editorial Screening Decision Support System

## Overview

ESDSS (Editorial Screening Decision Support System) is an AI-powered decision support system designed to automate and improve the editorial screening process using an intelligent multi-agent architecture.

## Installation

```bash
# Clone the repository
git clone https://github.com/niklas-silla/esdss.git
cd esdss

# Create and activate environment
conda create -n esdss
conda activate esdss

# Install dependencies
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

Create the manuscripts directory and copy your manuscripts into the folder.
(Each manuscript should be placed in a separate file)
```bash
# Create manuscript directory
mkdir data/manuscripts

# Start the workflow
python main.py
```

