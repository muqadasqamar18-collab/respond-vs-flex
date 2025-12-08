import os
import argparse
import json
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document

def extract_text(filepath):
    text = ""
    try:
        if filepath.lower().endswith('.pdf'):
            reader = PdfReader(filepath)
            # Use first 10 pages for LLM classification to give it enough context
            for page in reader.pages[:10]:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif filepath.lower().endswith('.docx'):
            doc = Document(filepath)
            # First 50 paragraphs
            for para in doc.paragraphs[:50]:
                text += para.text + "\n"
        elif filepath.lower().endswith('.doc'):
             pass
    except Exception as e:
        # print(f"Error reading {filepath}: {e}")
        pass
    return text

def classify_file_llm(filepath):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return json.dumps({"error": "GEMINI_API_KEY environment variable not set"})

    text = extract_text(filepath)
    if not text:
         return json.dumps({"error": f"Could not extract text from {filepath}"})

    filename = os.path.basename(filepath)

    # Configure Gemini
    genai.configure(api_key=api_key)

    # Attempt to use the requested model
    model_name = "gemini-2.5-pro"

    model = genai.GenerativeModel(model_name)

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
        return response.text
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify Grant Proposals using Gemini')
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='Files to classify')
    args = parser.parse_args()

    results = {}
    for f in args.files:
        if os.path.exists(f):
            result_json = classify_file_llm(f)
            try:
                results[f] = json.loads(result_json)
            except:
                results[f] = {"raw_output": result_json}
        else:
            results[f] = {"error": "File not found"}

    print(json.dumps(results, indent=2))
