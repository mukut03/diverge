import subprocess
import os
import time


def start_backend():
    """Start the FastAPI backend server."""
    global be
    be = subprocess.Popen([
        "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"
    ])


def start_frontend():
    """Start the Streamlit frontend server."""
    global fe
    fe = subprocess.Popen([
        "streamlit", "run", "frontend/streamlit_app.py", "--server.port", "8501"
    ])


def shutdown_servers():
    print("Shutting down servers...")
    try:
        if be:
            be.terminate()
        if fe:
            fe.terminate()
    except Exception as e:
        print(f"Error during shutdown: {e}")
    finally:
        time.sleep(1)  # Allow time to close gracefully

def main():
    try:
        print("Starting FastAPI backend...")
        start_backend()
        print("Starting Streamlit frontend...")
        start_frontend()

        # Wait for user interrupt
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Received exit signal. Stopping servers...")
        shutdown_servers()
        print("Servers stopped. Exiting...")
    except Exception as e:
        print(f"Unexpected error: {e}")
        shutdown_servers()

if __name__ == "__main__":
    main()