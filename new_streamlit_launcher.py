# new_streamlit_launcher.py
import sys
import os
import importlib.metadata
import shutil


def create_default_config():
    """Create default config.toml with the correct theme if it doesn't exist"""
    config_content = """[theme]
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
    return config_content


def setup_streamlit_config():
    """Set up Streamlit configuration in the running environment"""
    if getattr(sys, 'frozen', False):
        # If running as a frozen application
        base_dir = sys._MEIPASS

        # Create .streamlit directory in user's home if it doesn't exist
        user_config_dir = os.path.expanduser('~/.streamlit')
        os.makedirs(user_config_dir, exist_ok=True)

        # First try to copy bundled config
        bundled_config = os.path.join(base_dir, '.streamlit')
        config_file = os.path.join(user_config_dir, 'config.toml')

        if os.path.exists(bundled_config):
            # Copy bundled config
            bundled_config_file = os.path.join(bundled_config, 'config.toml')
            if os.path.exists(bundled_config_file):
                shutil.copy2(bundled_config_file, config_file)
                print("Copied bundled config file")
        else:
            # Create default config if none exists
            if not os.path.exists(config_file):
                with open(config_file, 'w') as f:
                    f.write(create_default_config())
                print("Created default config file")


def run_streamlit():
    """Run the Streamlit app properly"""
    try:
        import streamlit.web.cli as stcli

        # Setup configuration before starting Streamlit
        setup_streamlit_config()

        # Set environment variables
        os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        os.environ['STREAMLIT_SERVER_RUN_ON_SAVE'] = 'false'
        os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

        # Theme-specific environment variables
        os.environ['STREAMLIT_THEME_BASE'] = 'custom'
        os.environ['STREAMLIT_THEME_PRIMARY_COLOR'] = '#181839'
        os.environ['STREAMLIT_THEME_BACKGROUND_COLOR'] = '#284054'
        os.environ['STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR'] = '#0b1f35'
        os.environ['STREAMLIT_THEME_TEXT_COLOR'] = '#d3d3d3'
        os.environ['STREAMLIT_THEME_FONT'] = 'monospace'

        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        main_script_path = os.path.join(base_dir, "streamlit_app.py")
        print(f"Looking for Streamlit app at: {main_script_path}")

        if not os.path.exists(main_script_path):
            print(f"Error: Could not find {main_script_path}")
            print("Contents of base_dir:")
            for item in os.listdir(base_dir):
                print(f" - {item}")
            sys.exit(1)

        sys.argv = [
            "streamlit",
            "run",
            main_script_path,
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.serverAddress=localhost",
            "--server.headless=true",
            "--server.enableCORS=true",
            "--server.enableXsrfProtection=false",
            "--global.developmentMode=false",
            "--theme.base=custom",
            "--theme.primaryColor=#181839",
            "--theme.backgroundColor=#284054",
            "--theme.secondaryBackgroundColor=#0b1f35",
            "--theme.textColor=#d3d3d3",
            "--theme.font=monospace"
        ]

        print("Starting Streamlit...")
        sys.exit(stcli.main())

    except Exception as e:
        print(f"Error running Streamlit: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    run_streamlit()