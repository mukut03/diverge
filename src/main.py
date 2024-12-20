from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.services import analyze_journal_entry
from src.models import JournalRequest, JournalAnalysis

app = FastAPI(
    title="Diverge",
    description="Journaling with LLMs for neurodivergent users",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", response_model=JournalAnalysis)
async def process_journal_entry(request: JournalRequest):
    """
    Endpoint to analyze a journal entry.

    Args:
        request (JournalRequest): The journal entry request.

    Returns:
        JournalAnalysis: Emotional analysis and insights.
    """
    try:
        return analyze_journal_entry(request.entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
