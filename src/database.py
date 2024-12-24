# database.py
from sqlalchemy import create_engine, Column, Integer, String, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
import sys

# Create Base class for declarative models
Base = declarative_base()


class JournalEntry(Base):
    """SQLAlchemy model for journal entries"""
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String, nullable=False)
    emotions = Column(JSON, nullable=False)
    context = Column(String, nullable=False)
    needs = Column(JSON, nullable=False)
    action_plan = Column(JSON, nullable=False)
    reflection = Column(String, nullable=False)


def get_db_path():
    """Get the correct database path whether running as script or frozen exe"""
    try:
        if getattr(sys, 'frozen', False):
            # If running as compiled application
            base_path = os.path.dirname(sys._MEIPASS)
        else:
            # If running as script
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Create the db directory if it doesn't exist
        db_dir = os.path.join(base_path, 'db')
        os.makedirs(db_dir, exist_ok=True)

        # Construct database path
        db_path = os.path.join(db_dir, 'journal.db')
        print(f"Using database path: {db_path}")
        return f"sqlite:///{db_path}"
    except Exception as e:
        print(f"Error determining database path: {e}")
        # Fallback to local directory if there's an error
        return "sqlite:///journal.db"


# Set up database engine and session factory
DATABASE_URL = get_db_path()
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database, creating all tables if they don't exist"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")

        # Test database connection
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            print("Database connection test successful")

    except SQLAlchemyError as e:
        print(f"Database initialization error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during database initialization: {e}")
        raise


def get_recent_entries(db: SessionLocal, limit: int = 3):
    """Fetch the most recent journal entries"""
    try:
        return db.query(JournalEntry).order_by(JournalEntry.id.desc()).limit(limit).all()
    except SQLAlchemyError as e:
        print(f"Error fetching recent entries: {e}")
        return []