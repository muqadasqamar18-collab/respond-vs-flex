# Grant Proposal Classifier

This tool automates the classification of grant proposal documents into two distinct categories: **Respond (Type 1)** and **Flex (Type 2)**. It leverages the **Gemini 2.5 Pro** LLM to analyze the text content of PDF and DOCX files and provides a structured JSON output with the classification and reasoning.

## Classification Types

### 1. Respond (Type 1)
*   **Characteristics:** Structured forms, fill-in-the-blank templates, applications with rigid segmentation (e.g., Chapters, Appendices), or documents explicitly labeled as "Application Form" or "Template".
*   **Purpose:** These documents are typically designed for automated data extraction or direct filling of specific fields.

### 2. Flex (Type 2)
*   **Characteristics:** Unstructured narratives, Requests for Proposals (RFPs), guidelines, question lists, or complex forms that require a narrative response rather than simple field filling.
*   **Purpose:** These documents require the applicant to generate a custom document (e.g., a Word doc) to answer a list of questions or address specific criteria.

## Prerequisites

*   Python 3.8+
*   A Google Gemini API Key (with access to `gemini-2.5-pro` model)

## Installation

1.  Clone the repository.
2.  Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

You must set your Gemini API key as an environment variable before running the script.

**Linux/macOS:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

## Usage

Run the `classify_proposals.py` script by passing the file paths of the documents you want to classify. You can pass multiple files at once.

```bash
python classify_proposals.py path/to/document1.pdf path/to/document2.docx
```

### Example

```bash
python classify_proposals.py "Flex/QuestionList (1).pdf" "Respond/Application_Template.docx"
```

### Streamlit Web App

You can also run the graphical interface:

```bash
streamlit run app.py
```

This will open a web browser where you can upload files and view classification results interactively.

## Output

The tool returns a JSON object where the keys are the file paths and the values are the classification results.

**Example Output:**

```json
{
  "Flex/QuestionList (1).pdf": {
    "classification": "Flex (Type 2)",
    "reasoning": "The document is a list of questions asking for narrative descriptions of the project, with character limits specified, rather than a structured form to be filled out."
  },
  "Respond/Application_Template.docx": {
    "classification": "Respond (Type 1)",
    "reasoning": "This document is a rigid template with defined chapters and fillable sections, typical of a standard application form."
  }
}
```

## Troubleshooting

*   **Error: GEMINI_API_KEY environment variable not set**: Ensure you have exported the API key correctly in your terminal session.
*   **Model Not Found**: If `gemini-2.5-pro` is not available for your API key, the script may fail. You may need to edit `classify_proposals.py` to use a different model (e.g., `gemini-1.5-pro`) if you do not have access to the specific version requested.
