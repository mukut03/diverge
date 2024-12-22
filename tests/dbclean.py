import os
from sqlalchemy.orm import Session
from src.database import SessionLocal, JournalEntry


def clear_database():
    """Removes all entries from the database."""
    # Ensure the database file exists
    db_path = "./db/journal.db"
    if not os.path.exists(db_path):
        print("Database not found. Make sure it exists before running this script.")
        return

    # Connect to the database and clear all entries
    db: Session = SessionLocal()
    try:
        db.query(JournalEntry).delete()  # Delete all rows
        db.commit()  # Commit changes
        print("All entries have been successfully removed from the database.")
    except Exception as e:
        db.rollback()
        print(f"Error clearing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    clear_database()
