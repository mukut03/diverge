import streamlit as st
import requests

# API Configuration
ANALYZE_API_URL = "http://127.0.0.1:8000/analyze"
PROMPTS_API_URL = "http://127.0.0.1:8000/prompts"
EXPORT_API_URL = "http://127.0.0.1:8000/export-csv"

# Page Configuration
st.set_page_config(page_title="Diverge", page_icon="📝", layout="wide")

# Header Section: Title with Icon
st.markdown("""
<div style='display: flex; align-items: center; margin-bottom: 20px;'>
    <div style='font-size: 2rem; font-weight: bold;'>
        🦙 better-tell-llama
    </div>
</div>
""", unsafe_allow_html=True)

# Two-column Layout
col1, col2 = st.columns([0.25, 0.75])

# Initialize session state
if "prompts" not in st.session_state:
    st.session_state["prompts"] = []
if "current_prompt" not in st.session_state:
    st.session_state["current_prompt"] = 0

# Left Column: Description and Links
with col1:
    st.markdown("""
        <div style='text-align: left;'>
            <p style='font-size: 1.2rem; font-weight: bold; margin-bottom: 15px;'>
                This tool uses a llama3.2 running locally with ollama serve to help you journal and make sense.
            </p>
            <p style='font-size: 1rem; margin-bottom: 15px;'>
                Overcome overwhelming thoughts or feelings. Writing in the text box on the right helps to reframe your experiences and validate your emotions with compassion.
            </p>
            <p style='font-size: 1.1rem; margin-bottom: 15px;'>
                Designed to gently guide you toward understanding your emotions, offering clarity that can be hard to find in the moment.
            </p>
            <p style='font-size: 0.9rem; margin-bottom: 30px;'>
                If you're looking for a fresh perspective, emotional validation, or practical ways to move forward, you better-tell-llama🦙
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        f"<a style='display: block; text-align: center; margin-bottom: 10px;' href={'https://github.com/mukut03'}>GitHub</a>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<a style='display: block; text-align: center;' href={'https://linkedin.com/in/mukutm'}>LinkedIn</a>",
        unsafe_allow_html=True,
    )

# Right Column: Text Box and Buttons
with col2:
    # Text area for journal entry
    entry = st.text_area(
        "Journal Entry", label_visibility="hidden",
        placeholder="e.g., I feel stressed about work and unsure how to move forward...",
        height=500,
    )

    # Custom HTML and CSS for Proper Button Row
    st.markdown(
        """
        <style>
            .button-container {
                display: flex;
                justify-content: flex-start;
                gap: 10px; /* Controls spacing between buttons */
                margin-top: 10px; /* Adds spacing above the buttons */
            }
            .button-container button {
                flex-grow: 0;
                padding: 8px 16px;
            }
        </style>
        <div class="button-container">
            <form action="#" method="post" target="_self">
                <button type="submit" name="submit_entry">🦙 Submit Entry</button>
            </form>
            <form action="#" method="post" target="_self">
                <button type="submit" name="try_prompts">📋 Try Journal Prompts</button>
            </form>
            <form action="#" method="post" target="_self">
                <button type="submit" name="export_reports">📤 Export All Reports</button>
            </form>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Handle Button Clicks
    if st.session_state.get("submit_entry", False):
        if entry.strip():
            with st.spinner("Analyzing your journal entry..."):
                try:
                    response = requests.post(
                        ANALYZE_API_URL,
                        json={"entry": entry},
                        headers={"Content-Type": "application/json"},
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown("### dalai-llama🦙report")
                        st.json(result)
                    else:
                        st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the backend. Error: {e}")
        else:
            st.error("Please enter some text to analyze.")

    if st.session_state.get("try_prompts", False):
        try:
            response = requests.get(PROMPTS_API_URL)
            if response.status_code == 200:
                data = response.json()
                prompts = data.get("prompts", {}).get("prompts", [])
                if isinstance(prompts, list) and all(isinstance(p, str) for p in prompts):
                    st.session_state["prompts"] = prompts
                    st.session_state["current_prompt"] = 0
                else:
                    st.error("Invalid response format for prompts.")
            else:
                st.error("Not enough entries to generate prompts.")
        except Exception as e:
            st.error(f"Failed to fetch prompts. Error: {e}")

    if st.session_state.get("export_reports", False):
        response = requests.get(EXPORT_API_URL)
        if response.status_code == 200:
            st.download_button(
                label="📤 Export All Reports",
                data=response.content,
                file_name="journal_entries.csv",
                mime="text/csv"
            )
        else:
            st.error("No entries available to export.")

# Sidebar for prompts
if st.session_state["prompts"]:
    st.sidebar.markdown("### Suggested Journal Prompts")
    prompt_index = st.session_state["current_prompt"]

    # Display current prompt
    st.sidebar.markdown(f"**{st.session_state['prompts'][prompt_index]}**")

    # Buttons to cycle prompts
    col_prev, col_next = st.sidebar.columns([0.4, 0.4])
    with col_prev:
        if st.sidebar.button("← Previous") and prompt_index > 0:
            st.session_state["current_prompt"] -= 1
    with col_next:
        if st.sidebar.button("Next →") and prompt_index < len(st.session_state["prompts"])-1:
            st.session_state["current_prompt"] += 1

# Footer
st.markdown("---")
st.write(
    "This project is powered by AI and designed to provide actionable insights for self-reflection. "
    "Feel free to [contribute](#) or reach out for [collaboration](#)."
)
