from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define JournalEntry model
class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String, nullable=False)
    emotions = Column(JSON, nullable=False)
    context = Column(String, nullable=False)
    needs = Column(JSON, nullable=False)
    action_plan = Column(JSON, nullable=False)
    reflection = Column(String, nullable=False)

# Initialize SQLite database
DATABASE_URL = "sqlite:///./db/journal.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_recent_entries(db: SessionLocal, limit: int = 3):
    """
    Fetches the most recent journal entries from the database.
    """
    return db.query(JournalEntry).order_by(JournalEntry.id.desc()).limit(limit).all()
