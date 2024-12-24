# 1. build_all.py
import PyInstaller.__main__
import os
import sys
import streamlit
import uvicorn
import shutil
from pathlib import Path


def create_default_config():
    """Create default config.toml with the correct theme"""
    return """[theme]
primaryColor="#181839"
backgroundColor="#284054"
secondaryBackgroundColor="#0b1f35"
textColor="#d3d3d3"
font="monospace"

[server]
runOnSave = false
enableCORS = true
enableXsrfProtection = false

[global]
developmentMode = false
showWarningOnDirectExecution = false

[browser]
gatherUsageStats = false
"""


def ensure_clean_directory():
    """Ensure we have clean directories to work with"""
    paths = ['dist', 'build', 'temp_dist']
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)
        if path != 'build':  # We don't need to recreate build
            os.makedirs(path)


def build_backend():
    """Build the FastAPI backend"""
    print("Building backend server...")
    uvicorn_path = os.path.dirname(uvicorn.__file__)

    if not os.path.exists('db'):
        os.makedirs('db')

    PyInstaller.__main__.run([
        'backend_wrapper.py',
        '--onefile',
        '--name', 'fastapi_backend',
        '--distpath', './temp_dist',
        '--add-data', f'src{os.pathsep}src',
        '--add-data', f'db{os.pathsep}db',
        '--add-data', f'{uvicorn_path}/protocols{os.pathsep}uvicorn/protocols',
        '--add-data', f'{uvicorn_path}/lifespan{os.pathsep}uvicorn/lifespan',
        '--hidden-import', 'uvicorn.logging',
        '--hidden-import', 'uvicorn.loops',
        '--hidden-import', 'uvicorn.loops.auto',
        '--hidden-import', 'uvicorn.protocols',
        '--hidden-import', 'uvicorn.protocols.http',
        '--hidden-import', 'uvicorn.protocols.http.auto',
        '--hidden-import', 'uvicorn.protocols.websockets',
        '--hidden-import', 'uvicorn.protocols.websockets.auto',
        '--hidden-import', 'uvicorn.lifespan',
        '--hidden-import', 'uvicorn.lifespan.on',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'sqlalchemy.sql.default_comparator',
        '--hidden-import', 'sqlalchemy.ext.declarative',
        '--hidden-import', 'sqlalchemy.orm',
        '--hidden-import', 'sqlalchemy.pool',
        '--hidden-import', 'src.database',
        '--hidden-import', 'src.services',
        '--hidden-import', 'src.models',
        '--collect-all', 'uvicorn',
    ])


def build_frontend():
    """Build the Streamlit frontend with theme support"""
    print("Building frontend interface...")
    streamlit_path = os.path.dirname(streamlit.__file__)

    # Get Streamlit's paths
    static_path = os.path.join(streamlit_path, 'static')
    components_path = os.path.join(streamlit_path, 'components')

    # Ensure .streamlit directory exists with config
    if not os.path.exists('.streamlit'):
        os.makedirs('.streamlit')

    config_path = os.path.join('.streamlit', 'config.toml')
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write(create_default_config())

    PyInstaller.__main__.run([
        'new_streamlit_launcher.py',
        '--onefile',
        '--name', 'streamlit_frontend',
        '--distpath', './temp_dist',
        # Add data files
        '--add-data', f'streamlit_app.py{os.pathsep}.',
        '--add-data', f'.streamlit{os.pathsep}.streamlit',
        '--add-data', f'{static_path}{os.pathsep}streamlit/static',
        '--add-data', f'{components_path}{os.pathsep}streamlit/components',
        '--add-data', f'{streamlit_path}{os.pathsep}streamlit',
        # Hidden imports
        '--hidden-import', 'streamlit',
        '--hidden-import', 'streamlit.web.bootstrap',
        '--hidden-import', 'streamlit.web.server.server',
        '--hidden-import', 'streamlit.web.server',
        '--hidden-import', 'streamlit.runtime',
        '--hidden-import', 'streamlit.runtime.scriptrunner',
        '--hidden-import', 'streamlit.web.cli',
        '--hidden-import', 'streamlit.runtime.runtime',
        '--hidden-import', 'streamlit.runtime.caching',
        '--hidden-import', 'streamlit.runtime.secrets',
        '--hidden-import', 'streamlit.elements',
        '--hidden-import', 'streamlit.commands',
        '--hidden-import', 'streamlit.commands.page_config',
        '--hidden-import', 'streamlit.elements.image',
        '--hidden-import', 'streamlit.elements.pyplot',
        '--hidden-import', 'streamlit.elements.theme',
        '--hidden-import', 'streamlit.elements.layouts',
        '--hidden-import', 'streamlit.source_util',
        '--hidden-import', 'streamlit.config_util',
        '--hidden-import', 'streamlit.git_util',
        '--hidden-import', 'streamlit.watcher',
        '--hidden-import', 'watchdog',
        '--hidden-import', 'watchdog.observers',
        '--hidden-import', 'watchdog.events',
        '--hidden-import', 'packaging',
        '--hidden-import', 'packaging.version',
        '--hidden-import', 'importlib.metadata',
        # Essential metadata only
        '--copy-metadata', 'streamlit',
        '--copy-metadata', 'click',
        # Collect essential packages
        '--collect-all', 'streamlit',
        '--collect-all', 'packaging',
        '--collect-data', 'streamlit'
    ])


def create_launcher():
    """Create the combined launcher script"""
    print("Creating application launcher...")
    launcher_code = '''import os
import sys
import signal
import subprocess
import time
from pathlib import Path

def get_executable_path(name):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    if sys.platform.startswith("win"):
        name = f"{name}.exe"
    return os.path.join(base_path, name)

def main():
    print("Starting Diverge...")

    # Start backend
    backend_path = get_executable_path("fastapi_backend")
    print("Starting backend server...")
    backend_process = subprocess.Popen([backend_path])

    # Wait for backend to start
    print("Waiting for backend to initialize...")
    time.sleep(3)

    # Start frontend
    frontend_path = get_executable_path("streamlit_frontend")
    print("Starting frontend interface...")
    frontend_process = subprocess.Popen([frontend_path])

    def cleanup(signum=None, frame=None):
        print("\\nShutting down gracefully...")
        frontend_process.terminate()
        backend_process.terminate()
        try:
            frontend_process.wait(timeout=5)
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Force closing applications...")
            frontend_process.kill()
            backend_process.kill()
        print("Shutdown complete")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        backend_process.wait()
    except KeyboardInterrupt:
        cleanup()
    finally:
        cleanup()

if __name__ == "__main__":
    main()
'''

    with open('combined_launcher.py', 'w') as f:
        f.write(launcher_code)
    return Path('combined_launcher.py')


def build_combined():
    """Build the final combined executable"""
    print("Building final application...")
    PyInstaller.__main__.run([
        'combined_launcher.py',
        '--onefile',
        '--name', 'diverge',
        '--add-data', f'temp_dist/fastapi_backend{os.pathsep}.',
        '--add-data', f'temp_dist/streamlit_frontend{os.pathsep}.',
    ])


def cleanup():
    """Clean up temporary files and directories"""
    print("Cleaning up temporary files...")
    paths_to_remove = ['temp_dist', 'build', 'combined_launcher.py']
    spec_files = [f for f in os.listdir() if f.endswith('.spec')]

    for path in paths_to_remove:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Warning: Could not remove {path}: {e}")

    for spec_file in spec_files:
        try:
            os.remove(spec_file)
        except Exception as e:
            print(f"Warning: Could not remove {spec_file}: {e}")


def main():
    try:
        ensure_clean_directory()
        build_backend()
        build_frontend()
        create_launcher()
        build_combined()
        print("\nBuild successful! Your application is in the dist directory.")
        print("Run it with: ./dist/diverge")
    except Exception as e:
        print(f"\nError during build: {e}")
        raise
    finally:
        cleanup()


if __name__ == '__main__':
    main()