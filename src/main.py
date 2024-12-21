from fastapi import FastAPI, HTTPException, Depends, Response
from src.models import JournalRequest, JournalResponse
from sqlalchemy.orm import Session
from src.services import analyze_journal_entry, save_entry, get_all_entries, generate_journal_prompts
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


@app.get("/prompts")
def get_journal_prompts():
    """
    API to fetch suggested journal prompts based on recent entries.
    """
    prompts = generate_journal_prompts()
    if not prompts:
        raise HTTPException(status_code=400, detail="Not enough entries for prompts.")
    return {"prompts": prompts}


@app.get("/export-csv")
def export_entries_to_csv(db: Session = Depends(get_db)):
    """
    API to export all journal entries and analyses as a CSV file.
    """
    entries = get_all_entries(db)
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found.")

    # Use csv module to properly handle formatting
    output = []
    output.append(["id", "entry", "emotions", "context", "needs", "action_plan", "reflection"])  # CSV header

    for entry in entries:
        output.append([
            entry.id,
            entry.entry.replace("\n", " "),  # Replace newlines to avoid breaking rows
            ", ".join(entry.emotions),       # Flatten emotions list into a comma-separated string
            entry.context.replace("\n", " "),
            ", ".join(entry.needs),          # Flatten needs list
            ", ".join(entry.action_plan),    # Flatten action plan list
            entry.reflection.replace("\n", " ")
        ])

    # Generate CSV content
    csv_content = "\n".join([",".join(f'"{str(cell)}"' for cell in row) for row in output])

    # Return as downloadable CSV
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=journal_entries.csv"}
    )
