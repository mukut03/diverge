from fastapi import FastAPI, HTTPException, Depends
from src.models import JournalRequest, JournalResponse
from sqlalchemy.orm import Session
from src.services import analyze_journal_entry, save_entry, get_all_entries
from src.database import SessionLocal, init_db

# Initialize database
init_db()

# FastAPI app
app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/analyze", response_model=JournalResponse)
async def process_journal_entry(request: JournalRequest, db: Session = Depends(get_db)):
    """
    Process a journal entry and return structured analysis.
    """
    try:
        # Analyze the entry
        result = analyze_journal_entry(request.entry)

        # Save the result in the database
        save_entry(db, request.entry, result)

        # Return the structured response
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/entries")
async def get_entries(db: Session = Depends(get_db)):
    """
    Fetch all stored journal entries.
    """
    try:
        entries = get_all_entries(db)
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
