import os
import sys
from pathlib import Path
import uvicorn

# Add the application directory to sys.path
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, use sys._MEIPASS
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

# Import your FastAPI app
from src.main import app

if __name__ == "__main__":
    # Start uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )