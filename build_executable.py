import PyInstaller.__main__

PyInstaller.__main__.run([
    "--name", "diverge",
    "--onefile",
    "--console",
    "--add-data", "src/main.py:src/",
    "--add-data", "frontend/streamlit_app.py:frontend/",
    "--add-data", "db/journal.db:db/",
    "diverge.py"
])

print("Executable built successfully! Check the 'dist' folder.")
