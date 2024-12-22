import subprocess
import time

def start_backend():
    print("Starting FastAPI backend...")
    backend = subprocess.Popen(["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    return backend

def start_frontend():
    print("Starting Streamlit frontend...")
    frontend = subprocess.Popen(["streamlit", "run", "frontend/streamlit_app.py", "--server.port", "8501"])
    return frontend

def main():
    backend = start_backend()
    time.sleep(5)  # Wait for backend to start
    frontend = start_frontend()
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("Shutting down servers...")
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    main()
