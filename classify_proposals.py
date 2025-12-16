import os
import re
import argparse
import sys
from pypdf import PdfReader
from docx import Document

def extract_text(filepath):
    text = ""
    num_pages = 0
    try:
        if filepath.lower().endswith('.pdf'):
            reader = PdfReader(filepath)
            num_pages = len(reader.pages)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif filepath.lower().endswith('.docx'):
            doc = Document(filepath)
            num_pages = len(doc.paragraphs) // 50
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif filepath.lower().endswith('.doc'):
             pass
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        pass
    return text, num_pages

def calculate_complexity_score(text, num_pages, filename=""):
    score = 0
    # Heuristics
    if re.search(r'cover page|exe statement', filename, re.IGNORECASE):
        score += 15
    if re.search(r'table of contents|list of figures', text, re.IGNORECASE):
        score += 10
    if re.search(r'certification|ordinance|executive order|cfr|debarment|assessed valuation|obligation bond|debt security pledge', text, re.IGNORECASE):
        score += 15
    # Dimensions
    # Dimension 1: Structure
    dim1_score = 0
    if num_pages > 15: dim1_score += 15
    if re.search(r'loi|invitation required|separate budget justification|pre-award risk assessment', text, re.IGNORECASE): dim1_score += 10
    if all(k in text for k in ['background', 'methods', 'budget']): dim1_score += 5
    score += min(dim1_score, 25)
    # Dimension 2: Evidence
    if re.search(r'literature review|references|current scholarship|evidence base|irb approval|ethics review', text, re.IGNORECASE):
        score += 20
    # Dimension 3: Volume
    dim3_score = 0
    if len(text.split()) > 6000: dim3_score += 10
    if re.search(r'methodology section|research design|conceptual framework|indirect costs|salary cap|statistical power', text, re.IGNORECASE): dim3_score += 10
    score += min(dim3_score, 15)
    # Dimension 4: Specificity
    dim4_score = 0
    if re.search(r'rubric', text, re.IGNORECASE): dim4_score += 10
    if len(re.findall(r'(\b(what|why|how|describe|explain)\b.+(\band|or|if|then|but also)\b.+(\band|or|if|then|but also)\b)', text, re.IGNORECASE)) > 3: dim4_score += 10
    score += min(dim4_score, 15)
    # Remaining Dimensions...
    if re.search(r'year-by-year projections|5-year cash flow|quantifiable metrics|cost per|cost-effectiveness ratio|baseline data', text, re.IGNORECASE): score += 15
    if re.search(r'study section|peer review|scientific expertise|reviewer qualifications|consensus scoring', text, re.IGNORECASE): score += 15
    if re.search(r'ffr required|quarterly reporting|rppr|site visits|data safety monitoring|audit requirement|sam\.gov', text, re.IGNORECASE): score += 20
    if re.search(r'capacity assessment|oca|scoring matrix|track record verification|staff credential check|risk rating', text, re.IGNORECASE): score += 15
    if re.search(r'theory of change|logic model|logframe|assumptions section|baseline data|comparison group', text, re.IGNORECASE): score += 15
    if re.search(r'cost-effectiveness|cost per|line-item justification|cost estimation methodology|market benchmarks|indirect rate|nicra', text, re.IGNORECASE): score += 15
    if re.search(r'sustainability plan|exit strategy|revenue diversification|step-down funding|transition plan', text, re.IGNORECASE): score += 15
    if re.search(r'grants\.gov|era commons|aor registration|electronic signature|pdf specifications', text, re.IGNORECASE): score += 15
    if re.search(r'methodology section|research design|baseline data plan|comparison group|statistical analysis|external evaluator', text, re.IGNORECASE): score += 15

    return score

def separate_text_components(text):
    instruction_text = []
    question_text = []

    instruction_keywords = ['instruction', 'guidance', 'your response should', 'evaluation criteria', 'preamble', 'note', 'important', 'eligibility', 'submission guidelines']
    question_keywords = ['what', 'why', 'how', 'describe', 'explain', 'list', 'provide', 'question', 'application form', 'fillable', 'project narrative', 'budget', 'timeline', 'goals', 'objectives']

    for line in text.splitlines():
        line_lower = line.lower()
        is_instruction = any(keyword in line_lower for keyword in instruction_keywords)
        is_question = any(keyword in line_lower for keyword in question_keywords) or line.strip().endswith('?') or '___' in line or '[]' in line

        if is_question and not is_instruction:
            question_text.append(line)
        elif is_instruction and not is_question:
            instruction_text.append(line)
        elif is_question and is_instruction: # Ambiguous, default to question
            question_text.append(line)
        else: # Default to instruction
            instruction_text.append(line)

    return "\n".join(instruction_text), "\n".join(question_text)

def classify_file(filepath):
    filename = os.path.basename(filepath).lower()
    text, num_pages = extract_text(filepath)

    # --- Hard Switch Rules ---
    if re.search(r'chapter|appendix', filename, re.IGNORECASE): return "RESPOND"
    if re.search(r'letter of inquiry|loi', text, re.IGNORECASE) and (num_pages > 3 or re.search(r'methods|literature', text, re.IGNORECASE)): return "RESPOND"
    if re.search(r'budget justification form', text, re.IGNORECASE): return "RESPOND"
    if re.search(r'grants\.gov|era commons|study section|quarterly reporting', text, re.IGNORECASE): return "RESPOND"
    if re.search(r'theory of change required|capacity assessment.*scoring', text, re.IGNORECASE): return "RESPOND"
    if num_pages <= 3 and re.search(r'email submission', text, re.IGNORECASE) and re.search(r'any format', text, re.IGNORECASE): return "FLEX"
    if re.search(r'community review', text, re.IGNORECASE): return "FLEX"
    if re.search(r'annual or final report only', text, re.IGNORECASE): return "FLEX"

    # --- Iceberg Analysis ---
    instruction_text, question_text = separate_text_components(text)

    instruction_score = calculate_complexity_score(instruction_text, num_pages, filename)
    question_score = calculate_complexity_score(question_text, num_pages, filename)

    gap_score = instruction_score - question_score

    final_score = (instruction_score * 0.6) + (question_score * 0.4) # Weighted average

    if 15 <= gap_score <= 30:
        final_score += 10
    elif gap_score > 30:
        final_score += 20

    # --- Final Classification ---
    if final_score >= 60:
        return "RESPOND"
    else:
        return "FLEX"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify Grant Proposals')
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='Files to classify')
    args = parser.parse_args()

    for f in args.files:
        if os.path.exists(f):
            result = classify_file(f)
            print(f"{f}: {result}")
        else:
            result = classify_file(f)
            print(f"{f} (File not found, classified by name/default): {result}")
