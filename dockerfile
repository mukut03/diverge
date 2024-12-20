# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Add Tini (a lightweight process manager)
RUN apt-get update && apt-get install -y tini

# Set Tini as the entrypoint
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start both services
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
