# Diverge

Diverge is a journaling tool designed specifically for neurodivergent individuals to help with emotional regulation. By focusing on simplicity and clarity, Diverge provides users with a streamlined way to process and reflect on their mental states, experiences, and tasks without feeling overwhelmed.

## Screenshots
![Example Entry](usage/images/entry.png)
![Example Response](usage/images/response.png)

## Features
- **Emotional Regulation**: Identifies complex emotions, causes, and triggers expressed in the entry, providing opportunities for effective cognitive reappraisal.
- **Personalized Prompts**: Generates journaling prompts for users, based on their three most recent entries.
- **Export Entries and Reports**: All entries and their reports are persisted locally. Users can export all entries and reports to date into a CSV.
- **Streamlined Input and Output**: Avoids excessive outputs and complexity, ensuring users receive actionable insights without additional cognitive burden.
- **AI-Powered Analysis**: Powered by a Llama 3.2 7b, running locally on Ollama, to ensure privacy and responsiveness. Free of cost and not part of the daily LLM carbon footprint (ChatGPT emits approx. 43,200 kilograms of CO2 each day).
- **Minimalist Frontend**: Built with Streamlit, providing a clean and intuitive interface.
- **Executable Version**: Easily run Diverge as a standalone executable without requiring manual setup.

## How It Works
1. **Input**: Users write candid journal entries about their thoughts, feelings, or experiences.
2. **Processing**: The Llama 3.2 model processes the input, identifies emotions, contexts, and triggers, along with opportunities for effective cognitive reappraisal.
3. **Output**: The user receives feedback that emphasizes emotional clarity and self-compassion, helping them better understand their mental states.

## Why Diverge?
Diverge is built with the needs of neurodivergent individuals in mind, offering:
- A non-judgmental space for self-expression.
- Tools to foster emotional clarity and understanding.
- A focus on self-compassion over performance or productivity.

## Technologies Used
- **Backend**: FastAPI and Python 3.11.
- **Frontend**: Streamlit for an interactive and accessible user interface.
- **Local LLM**: Ensures privacy and data security by processing everything locally.
- **Database**: SQLite for persistence.
- **Executable Packaging**: PyInstaller for standalone deployment.

## Installation
To run Diverge on your local machine, follow these steps:

### Option 1: Using the Executable
1. **Download Executable**:
   Download the pre-built executable from the releases page.

2. **Run the Executable**:
   ```bash
   ./dist/diverge
   ```

3. **Access the Application**:
   Navigate to `http://localhost:8501` to start using Diverge.

### Option 2: Build from Source
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mukut03/diverge.git
   cd diverge
   ```

2. **Set Up the Environment**:
   Ensure you have Python installed (version 3.11) and set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama**:
   Install Ollama and start Llama 3.2.

5. **Build Executable**:
   ```bash
   python build_executable.py
   ```

6. **Launch Diverge**:
   ```bash
   dist/diverge
   ```

7. **Access the Application**:
   Navigate to `http://localhost:8501` to start using Diverge.

## Contributing
Contributions are welcome. Journaling is one way to practice emotional regulation with local LLMs. If you have ideas for features or want to improve the existing code, please submit a pull request or open an issue in the repository.

## License
Diverge is licensed under the MIT License. See `LICENSE` for more details.

---

### Contact
For questions or support, please reach out to [mukutm2@illinois.edu] or open an issue in this repository.

