import streamlit as st
import requests

# API Configuration
API_URL = "http://127.0.0.1:8000/analyze"

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

# Add spacing between the description and the button
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Two-column Layout
col1, col2 = st.columns([0.25, 0.75])  # Adjusted column ratio

# Initialize session state for error handling
if "button_pressed" not in st.session_state:
    st.session_state["button_pressed"] = False


# Left Column: Description and Links
with col1:
    st.markdown("""
        <div style='text-align: left;'>
            <p style='font-size: 1.2rem; font-weight: bold; margin-bottom: 15px;'>
                this tool uses a llama3.2 running locally with ollama serve to help you journal and make sense
            </p>
            <p style='font-size: 1rem; margin-bottom: 15px;'>
                overcome overwhelming thoughts or feelings. writing in the text box on the right helps to reframe your experiences and validate your emotions with compassion.
            </p>
            <p style='font-size: 1.1rem; margin-bottom: 15px;'>
                designed to gently guide you toward understanding your emotions, offering the clarity that can be hard to find in the moment.
            </p>
            <p style='font-size: 0.9rem;'>
                if you're looking for a fresh perspective, emotional validation, or practical ways to move forward, you better-tell-llama🦙
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        f"<a style='display: block; text-align: center;' href={'https://github.com/mukut03'}>GitHub</a>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<a style='display: block; text-align: center;' href={'https://linkedin.com/mukutm'}>LinkedIn</a>",
        unsafe_allow_html=True,
    )

# Right Column: Text Box and Results
with col2:
    # Text entry box
    entry = st.text_area(
        "Journal Entry", label_visibility="hidden",
        placeholder="e.g., I feel stressed about work and unsure how to move forward...",
        height=500,
    )

    # Analyze Button
    if st.button("🦙🦙🦙"):
        if entry.strip():
            with st.spinner("Analyzing your journal entry..."):
                try:
                    response = requests.post(
                        API_URL,
                        json={"entry": entry},
                        headers={"Content-Type": "application/json"},
                    )
                    if response.status_code == 200:
                        result = response.json()["analysis"]

                        # Results Box
                        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Add space
                        st.markdown("""
                        <div style="background-color: #485380; padding: 10px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
                            <h4>dalai-llama🦙report</h4>
                            <p>{}</p>
                        </div>
                        """.format(result), unsafe_allow_html=True)

                    else:
                        st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the backend. Error: {e}")
        else:
            st.error("Please enter some text to analyze.")

# Footer
st.markdown("---")
st.write(
    "This project is powered by AI and designed to provide actionable insights for self-reflection. "
    "Feel free to [contribute](#) or reach out for [collaboration](#)."
)
