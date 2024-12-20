import requests
import logging
from src.config import settings
from src.prompts import generate_analysis_prompt
from src.models import JournalAnalysis


def call_llama(prompt: str) -> str:
    """
    Calls the Ollama API with the given prompt and retrieves the response.

    Args:
        prompt (str): The input prompt for the Ollama model.

    Returns:
        str: The content of the response message.
    """
    url = settings.OLLAMA_URL  # URL defined in config.py

    data = {
        "model": settings.OLLAMA_MODEL,  # Llama model name (e.g., "llama2" or "llama3")
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,  # We don't need streaming for this use case
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()["message"]["content"]

    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling Ollama API: {e}")
        raise RuntimeError("Failed to communicate with the Ollama API") from e


def analyze_journal_entry(entry: str) -> JournalAnalysis:
    """
    Analyzes the journal entry using the Llama model.

    Args:
        entry (str): The journal entry to analyze.

    Returns:
        JournalAnalysis: Structured analysis response.
    """
    try:
        # Generate the structured prompt for analysis
        prompt = generate_analysis_prompt(entry)

        # Call the Ollama model with the generated prompt
        analysis_response = call_llama(prompt)

        # Process the response (you can add more sophisticated parsing if needed)
        return JournalAnalysis(
            analysis=analysis_response,
            emotions=["uncertainty", "reflection"],  # Replace with dynamic values if parsing is added
            confidence=0.85  # Replace with actual confidence if provided
        )

    except Exception as e:
        logging.error(f"Analysis error: {e}")
        raise RuntimeError("Failed to analyze the journal entry") from e
