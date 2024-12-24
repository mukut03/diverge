# src/main.py
from fastapi import FastAPI, HTTPException, Depends, Response
from src.models import JournalRequest, JournalResponse
from sqlalchemy.orm import Session
from src.services import analyze_journal_entry, save_entry, get_all_entries, generate_journal_prompts
from src.database import SessionLocal, init_db
import csv
from io import StringIO

# FastAPI app
app = FastAPI(
    title="Journal Analysis API",
    description="API for analyzing and managing journal entries"
)


# Move database initialization to startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    print("Initializing database...")
    init_db()
    print("Database initialization complete")


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}


@app.post("/analyze", response_model=JournalResponse)
async def process_journal_entry(request: JournalRequest, db: Session = Depends(get_db)):
    """Process a journal entry and return structured analysis."""
    try:
        # Analyze the entry
        result = analyze_journal_entry(request.entry)

        # Save the result in the database
        save_entry(db, request.entry, result)

        # Return the structured response
        return result

    except Exception as e:
        print(f"Error processing journal entry: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/entries")
async def get_entries(db: Session = Depends(get_db)):
    """Fetch all stored journal entries."""
    try:
        entries = get_all_entries(db)
        return entries
    except Exception as e:
        print(f"Error fetching entries: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prompts")
def get_journal_prompts():
    """Fetch suggested journal prompts based on recent entries."""
    prompts = generate_journal_prompts()
    if not prompts:
        raise HTTPException(status_code=400, detail="Not enough entries for prompts.")
    return {"prompts": prompts}


@app.get("/export-csv")
def export_entries_to_csv(db: Session = Depends(get_db)):
    """Export all journal entries and analyses as a CSV file."""
    try:
        entries = get_all_entries(db)
        if not entries:
            raise HTTPException(status_code=404, detail="No entries found.")

        # Create a StringIO object to write CSV data
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)

        # Write header
        writer.writerow(["id", "entry", "emotions", "context", "needs", "action_plan", "reflection"])

        # Write entries
        for entry in entries:
            writer.writerow([
                entry.id,
                entry.entry.replace("\n", " "),
                ", ".join(entry.emotions),
                entry.context.replace("\n", " "),
                ", ".join(entry.needs),
                ", ".join(entry.action_plan),
                entry.reflection.replace("\n", " ")
            ])

        # Get the CSV content
        csv_content = output.getvalue()
        output.close()

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=journal_entries.csv"}
        )
    except Exception as e:
        print(f"Error exporting CSV: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))