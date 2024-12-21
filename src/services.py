import requests
import logging
from src.config import settings
from src.prompts import generate_user_prompt, generate_system_prompt
from src.models import JournalAnalysis
from src.database import SessionLocal, JournalEntry
from sqlalchemy.orm import Session
from pydantic import ValidationError


def save_entry(db: Session, entry: str, analysis: JournalAnalysis):
    """
    Saves the journal entry and structured analysis to the database.
    """
    db_entry = JournalEntry(
        entry=entry,
        emotions=analysis.emotions,
        context=analysis.context,
        needs=analysis.needs,
        action_plan=analysis.action_plan,
        reflection=analysis.reflection,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_all_entries(db: Session):
    """
    Fetches all journal entries from the database.
    """
    return db.query(JournalEntry).all()


def analyze_journal_entry(entry: str) -> JournalAnalysis:
    """
    Analyzes the journal entry using the Llama model with structured outputs.

    Args:
        entry (str): The journal entry to analyze.

    Returns:
        JournalAnalysis: Structured analysis response.
    """
    try:
        # Prepare prompts
        system_prompt = generate_system_prompt()
        user_prompt = generate_user_prompt(entry)

        # Prepare the request payload
        data = {
            "model": settings.OLLAMA_MODEL,
            "prompt": f"{system_prompt}\n{user_prompt}",
            "format": "json",  # Enforce structured output
            "stream": False
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Make the API call
        response = requests.post(settings.OLLAMA_URL, headers=headers, json=data)
        response.raise_for_status()  # Handle HTTP errors

        # Parse and validate the response using Pydantic
        structured_response = JournalAnalysis.model_validate_json(response.json()["response"])
        return structured_response

    except ValidationError as ve:
        # Handle schema validation errors
        logging.error(f"Schema validation error: {ve}")
        raise RuntimeError("Response did not match the expected schema.") from ve

    except requests.exceptions.RequestException as e:
        # Handle network or API call errors
        logging.error(f"Error calling Ollama API: {e}")
        raise RuntimeError("Failed to communicate with the Ollama API") from e

    except Exception as e:
        logging.error(f"Analysis error: {e}")
        raise RuntimeError("Failed to analyze the journal entry") from e
