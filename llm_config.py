"""
llm_config.py
--------------
Central Orchestration of all LLMs (Ollama, OpenAI, etc.)
To easily change provider and model.
"""

from typing import Literal, Optional
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

# === LLM PROVIDER ===
ACTIVE_PROVIDER: Literal["ollama", "openai"] = "ollama"

# === MODEL-TYPE ===
ACTIVE_MODE: Literal["simple", "reasoning"] = "simple"

# === PARAMETER ===
DEFAULT_TEMPERATURE = 0
DEFAULT_MAX_TOKENS = 4096

# --- Ollama Modelle ---
OLLAMA_MODELS = {
    "simple": "gpt-oss:120b",
    "reasoning": "gpt-oss:120b"
}

# --- OpenAI Modelle ---
OPENAI_MODELS = {
    "simple": "gpt-4o-mini",
    "reasoning": "gpt-4o"
}


# ===========================================================
# FACTORY: get_llm()
# ===========================================================

def get_llm(mode: Optional[str] = None):
    """
    Returns a LLM instance based on global or specified configuration.
    """
    mode = mode or ACTIVE_MODE

    if ACTIVE_PROVIDER == "ollama":
        model = OLLAMA_MODELS[mode]
        return ChatOllama(
            model=model, 
            temperature=DEFAULT_TEMPERATURE, 
            base_url="http://localhost:11434"
            )

    elif ACTIVE_PROVIDER == "openai":
        model = OPENAI_MODELS[mode]
        return ChatOpenAI(
            model=model,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS,
        )