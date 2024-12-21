from src.database import SessionLocal
from src.services import get_all_entries

# Connect to the database
db = SessionLocal()

# Fetch all entries
entries = get_all_entries(db)

# Print all entries for verification
for entry in entries:
    print(f"ID: {entry.id}")
    print(f"Entry: {entry.entry}")
    print(f"Emotions: {entry.emotions}")
    print(f"Context: {entry.context}")
    print(f"Needs: {entry.needs}")
    print(f"Action Plan: {entry.action_plan}")
    print(f"Reflection: {entry.reflection}")
    print("------")

# Close the database session
db.close()
