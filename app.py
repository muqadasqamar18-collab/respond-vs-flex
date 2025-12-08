import streamlit as st
import os
import json
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document
import io

# --- Helper Functions ---

def extract_text_from_file(uploaded_file):
    """Extracts text from a file-like object (PDF or DOCX)."""
    text = ""
    try:
        if uploaded_file.name.lower().endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            # Use first 10 pages for LLM classification
            for page in reader.pages[:10]:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif uploaded_file.name.lower().endswith('.docx'):
            doc = Document(uploaded_file)
            # First 50 paragraphs
            for para in doc.paragraphs[:50]:
                text += para.text + "\n"
    except Exception as e:
        st.error(f"Error reading {uploaded_file.name}: {e}")
        return None
    return text

def classify_proposal(text, filename, api_key):
    """Calls Gemini to classify the proposal text."""
    if not text:
        return None

    # Configure Gemini
    genai.configure(api_key=api_key)

    # Use the requested model
    model_name = "gemini-2.5-pro"

    try:
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        # Fallback handling or error reporting
        return {"error": f"Failed to initialize model {model_name}: {str(e)}"}

    prompt = f"""
    Analyze the following text extracted from a grant proposal document.
    Classify it into one of two types based on these definitions:

    1. **Respond (Type 1)**: Structured forms, fill-in-the-blank templates, applications with rigid segmentation (Chapters, Appendices), or documents explicitly labeled as "Application Form" or "Template". These are usually meant for automated data extraction or direct filling.
    2. **Flex (Type 2)**: Unstructured narratives, Request for Proposals (RFP), guidelines, question lists, or complex forms that require a narrative response rather than simple field filling.

    Filename: {filename}

    Text Snippet:
    {text[:5000]}

    Return a valid JSON object with exactly two keys:
    - "classification": "Flex (Type 2)" or "Respond (Type 1)"
    - "reasoning": A brief explanation of why this classification was chosen.
    """

    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

# --- Streamlit UI ---

st.set_page_config(page_title="Grant Proposal Classifier", layout="wide")

st.title("Grant Proposal Classifier")
st.markdown("""
This tool classifies grant documents into **Respond (Type 1)** or **Flex (Type 2)** using Gemini 2.5 Pro.
""")

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")

    # Check if API key is in env, otherwise ask for it
    env_api_key = os.environ.get("GEMINI_API_KEY")
    api_key_input = st.text_input("Gemini API Key", value=env_api_key if env_api_key else "", type="password")

    if not api_key_input:
        st.warning("Please provide a Gemini API Key to proceed.")

# Main Interface
uploaded_files = st.file_uploader("Upload Grant Proposals (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files and st.button("Classify Documents"):
    if not api_key_input:
        st.error("API Key is required!")
    else:
        st.subheader("Classification Results")

        # Create columns for results
        cols = st.columns(2)

        for i, uploaded_file in enumerate(uploaded_files):
            with st.spinner(f"Processing {uploaded_file.name}..."):
                text = extract_text_from_file(uploaded_file)
                if text:
                    result = classify_proposal(text, uploaded_file.name, api_key_input)

                    # Determine which column to place the result in
                    col = cols[i % 2]

                    with col:
                        with st.container(border=True):
                            st.markdown(f"### {uploaded_file.name}")

                            if "error" in result:
                                st.error(result["error"])
                            else:
                                classification = result.get("classification", "Unknown")
                                reasoning = result.get("reasoning", "No reasoning provided.")

                                # Visual badge for classification
                                if "Type 1" in classification:
                                    st.info(f"**{classification}**")
                                else:
                                    st.success(f"**{classification}**")

                                st.write(reasoning)
                                st.json(result) # Show raw JSON expandable
