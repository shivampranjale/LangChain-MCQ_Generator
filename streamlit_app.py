"""
Streamlit UI for MCQ Generator application.
"""

import streamlit as st
import os
from datetime import datetime
from pathlib import Path
import tempfile
from dotenv import load_dotenv

# Load environment variables from secrets folder
env_path = Path(__file__).parent / 'secrets' / '.env'
load_dotenv(env_path)

from config import DEFAULT_TOPIC_DOMAIN
from models import initialize_model
from pdf_processor import read_pdf
from chains import create_summary_chain, create_mcq_chain
from utils import save_output

# Set page configuration
st.set_page_config(
    page_title="MCQ Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    [data-testid="stAppViewContainer"] {
        padding-top: 0rem;
    }
    header {
        display: none;
    }
    .stMarkdown {
        margin: 0;
        padding: 0;
    }
    h1 {
        margin: 0 !important;
        padding: 0 !important;
    }
    .stTitle {
        text-align: center;
        color: #1f77b4;
    }
    .mcq-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .mcq-scroll {
        height: 500px;
        overflow-y: auto;
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.6;
    }
    .mcq-scroll::-webkit-scrollbar {
        width: 8px;
    }
    .mcq-scroll::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    .mcq-scroll::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    .mcq-scroll::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #17a2b8;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('GOOGLE_API_KEY', '')

if 'model' not in st.session_state:
    st.session_state.model = None

if 'mcq_result' not in st.session_state:
    st.session_state.mcq_result = None

if 'content_summary' not in st.session_state:
    st.session_state.content_summary = None

if 'study_material' not in st.session_state:
    st.session_state.study_material = None

# Debug: Check if API key is loaded
if not st.session_state.api_key:
    st.warning("⚠️ API Key not found in environment. Checking environment variables...")
    # Display available env vars for debugging
    with st.expander("🔍 Debug: Environment Variables"):
        st.write(f"GOOGLE_API_KEY = {os.getenv('GOOGLE_API_KEY', 'NOT FOUND')}")
        st.write(f".env file path: {env_path}")
        st.write(f".env file exists: {env_path.exists()}")
        st.write(f"Current working directory: {os.getcwd()}")
        # Show all environment variables that contain 'API' or 'KEY'
        all_vars = {k: v[:50] + '...' if len(str(v)) > 50 else v for k, v in os.environ.items() if 'API' in k or 'KEY' in k}
        st.write(f"All API/KEY variables: {all_vars if all_vars else 'None found'}")


# Main title
st.markdown("<h1 style='text-align: center; color: #1f77b4; margin: 0; padding: 0.2rem;'>📚 MCQ Generator</h1>", unsafe_allow_html=True)

# Initialize model if API key is available
if st.session_state.api_key and st.session_state.model is None:
    try:
        st.session_state.model = initialize_model(st.session_state.api_key)
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")

# SIDEBAR - Input Section
st.sidebar.markdown("### 📤 Upload & Configure")

# PDF Upload
uploaded_file = st.sidebar.file_uploader(
    "Upload PDF File",
    type=['pdf'],
    help="Select a PDF file to extract study material"
)

if uploaded_file is not None:
    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name
    
    # Process PDF
    try:
        st.session_state.study_material = read_pdf(tmp_path)
        st.sidebar.markdown('<div class="info-message">✓ PDF uploaded successfully</div>', unsafe_allow_html=True)
        st.sidebar.caption(f"📄 File: {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")
        
        # Clean up temp file
        os.remove(tmp_path)
    except Exception as e:
        st.sidebar.error(f"Error reading PDF: {str(e)}")

st.sidebar.divider()

# Topic Input
st.sidebar.markdown("### 📝 Topic Configuration")
topic = st.sidebar.text_input(
    "Enter Topic",
    placeholder=f"e.g., {DEFAULT_TOPIC_DOMAIN}",
    help="Enter the topic for which you want to generate MCQs"
)

st.sidebar.divider()

# Generate Button
col1, col2 = st.sidebar.columns([1, 1])

with col1:
    generate_btn = st.sidebar.button(
        "🚀 Generate MCQs",
        use_container_width=True,
        type="primary"
    )

with col2:
    save_btn = st.sidebar.button(
        "💾 Save Output",
        use_container_width=True,
        disabled=(st.session_state.mcq_result is None)
    )

# Process MCQ Generation
if generate_btn:
    if st.session_state.study_material is None:
        st.sidebar.error("⚠️ Please upload a PDF file first")
    elif not topic.strip():
        st.sidebar.error("⚠️ Please enter a topic")
    elif st.session_state.model is None:
        st.sidebar.error("⚠️ Model not initialized. Check API key.")
    else:
        with st.spinner("🔄 Generating MCQs..."):
            try:
                # Create chains
                summary_chain = create_summary_chain(st.session_state.model)
                mcq_chain = create_mcq_chain(st.session_state.model)
                
                # Summarize content
                st.session_state.content_summary = summary_chain.invoke({
                    'study_material': st.session_state.study_material
                })
                
                # Generate MCQs
                st.session_state.mcq_result = mcq_chain.invoke({
                    'content_summary': st.session_state.content_summary,
                    'topic': topic,
                })
                
            except Exception as e:
                st.error(f"Error generating MCQs: {str(e)}")

# Save Output
if save_btn and st.session_state.mcq_result:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic.replace(" ", "_").replace("/", "_")
        
        # Save files
        summary_path = f"summary_{timestamp}.txt"
        mcq_path = f"mcq_{safe_topic}_{timestamp}.txt"
        
        save_output(st.session_state.content_summary, summary_path)
        save_output(st.session_state.mcq_result, mcq_path)
        
        st.sidebar.markdown(f'<div class="success-message">✓ Output saved successfully!</div>', unsafe_allow_html=True)
        st.sidebar.caption(f"📁 Files: {summary_path}, {mcq_path}")
    except Exception as e:
        st.error(f"Error saving output: {str(e)}")

# Debug section
if not st.session_state.api_key:
    st.sidebar.warning("⚠️ API Key not found in environment. Checking environment variables...")
    # Display available env vars for debugging
    with st.sidebar.expander("🔍 Debug: Environment Variables"):
        st.write(f"GOOGLE_API_KEY = {os.getenv('GOOGLE_API_KEY', 'NOT FOUND')}")
        st.write(f".env file path: {env_path}")
        st.write(f".env file exists: {env_path.exists()}")
        st.write(f"Current working directory: {os.getcwd()}")
        # Show all environment variables that contain 'API' or 'KEY'
        all_vars = {k: v[:50] + '...' if len(str(v)) > 50 else v for k, v in os.environ.items() if 'API' in k or 'KEY' in k}
        st.write(f"All API/KEY variables: {all_vars if all_vars else 'None found'}")

# MAIN CONTENT - MCQ Display
st.divider()
st.markdown("### 📖 Generated MCQs")

if st.session_state.mcq_result is None:
    st.info("📤 Use the sidebar to upload a PDF, enter a topic, and click 'Generate MCQs' to see the results here.")
else:
    # Display MCQs in scrollable container with full width
    st.markdown(f'<div class="mcq-scroll">{st.session_state.mcq_result}</div>', unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9em;'>
    <p>MCQ Generator v1.0 | Powered by LangChain & Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
