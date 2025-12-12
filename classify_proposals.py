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

def classify_file(filepath):
    filename = os.path.basename(filepath).lower()
    text, num_pages = extract_text(filepath)
    text = text.lower()

    # --- Hard Switch Rules ---
    if re.search(r'chapter|appendix', filename, re.IGNORECASE):
        return "RESPOND"
    if re.search(r'letter of inquiry|loi', text, re.IGNORECASE) and (num_pages > 3 or re.search(r'methods|literature', text, re.IGNORECASE)):
        return "RESPOND"
    if re.search(r'budget justification form', text, re.IGNORECASE):
        return "RESPOND"
    if re.search(r'grants\.gov|era commons|study section|quarterly reporting', text, re.IGNORECASE):
        return "RESPOND"
    if re.search(r'theory of change required|capacity assessment.*scoring', text, re.IGNORECASE):
        return "RESPOND"
    if num_pages <= 3 and re.search(r'email submission', text, re.IGNORECASE) and re.search(r'any format', text, re.IGNORECASE):
        return "FLEX"
    if re.search(r'community review', text, re.IGNORECASE):
        return "FLEX"
    if re.search(r'annual or final report only', text, re.IGNORECASE):
        return "FLEX"

    # --- Scoring Based on Dimensions and Heuristics ---
    respond_score = 0

    # Heuristics (points reduced to be less dominant)
    if re.search(r'cover page|exe statement', filename, re.IGNORECASE):
        respond_score += 15
    if re.search(r'table of contents|list of figures', text, re.IGNORECASE):
        respond_score += 10
    if re.search(r'certification|ordinance|executive order|cfr|debarment|assessed valuation|obligation bond|debt security pledge', text, re.IGNORECASE):
        respond_score += 15

    # Dimension 1: Application Structure & Gating (+25 pts)
    dim1_score = 0
    if num_pages > 15:
        dim1_score += 15
    if re.search(r'loi|invitation required|separate budget justification|pre-award risk assessment', text, re.IGNORECASE):
        dim1_score += 10
    if all(keyword in text for keyword in ['background', 'methods', 'budget']):
        dim1_score += 5
    respond_score += min(dim1_score, 25)

    # Dimension 2: External Evidence Requirement (+20 pts)
    dim2_score = 0
    if re.search(r'literature review|references|current scholarship|evidence base|irb approval|ethics review', text, re.IGNORECASE):
        dim2_score += 20
    respond_score += min(dim2_score, 20)

    # Dimension 3: Writing Effort & Volume (+15 pts)
    dim3_score = 0
    if len(text.split()) > 6000:
        dim3_score += 10
    if re.search(r'methodology section|research design|conceptual framework|indirect costs|salary cap|statistical power', text, re.IGNORECASE):
        dim3_score += 10
    respond_score += min(dim3_score, 15)

    # Dimension 4: Question Specificity (+15 pts)
    dim4_score = 0
    if re.search(r'rubric', text, re.IGNORECASE):
        dim4_score += 10
    compound_questions = 0
    for line in text.splitlines():
        if re.search(r'what|why|how|describe|explain', line, re.IGNORECASE):
            if len(re.findall(r'and|or|if|then|but also', line, re.IGNORECASE)) >= 2:
                compound_questions += 1
    if compound_questions > 3:
        dim4_score += 10
    respond_score += min(dim4_score, 15)

    # Dimension 5: Demonstrable Outcomes & Metrics (+15 pts)
    dim5_score = 0
    if re.search(r'year-by-year projections|5-year cash flow|quantifiable metrics|cost per|cost-effectiveness ratio|baseline data', text, re.IGNORECASE):
        dim5_score += 15
    respond_score += min(dim5_score, 15)

    # Dimension 6: Reviewer Expertise (+15 pts)
    dim6_score = 0
    if re.search(r'study section|peer review|scientific expertise|reviewer qualifications|consensus scoring', text, re.IGNORECASE):
        dim6_score += 15
    respond_score += min(dim6_score, 15)

    # Dimension 7: Post-Award Monitoring (+20 pts)
    dim7_score = 0
    if re.search(r'ffr required|quarterly reporting|rppr|site visits|data safety monitoring|audit requirement|sam\.gov', text, re.IGNORECASE):
        dim7_score += 20
    respond_score += min(dim7_score, 20)

    # Dimension 8: Organizational Capacity Assessment (+15 pts)
    dim8_score = 0
    if re.search(r'capacity assessment|oca|scoring matrix|track record verification|staff credential check|risk rating', text, re.IGNORECASE):
        dim8_score += 15
    respond_score += min(dim8_score, 15)

    # Dimension 9: Evidence Framework (+15 pts)
    dim9_score = 0
    if re.search(r'theory of change|logic model|logframe|assumptions section|baseline data|comparison group', text, re.IGNORECASE):
        dim9_score += 15
    respond_score += min(dim9_score, 15)

    # Dimension 10: Budget Justification (+15 pts)
    dim10_score = 0
    if re.search(r'cost-effectiveness|cost per|line-item justification|cost estimation methodology|market benchmarks|indirect rate|nicra', text, re.IGNORECASE):
        dim10_score += 15
    respond_score += min(dim10_score, 15)

    # Dimension 11: Sustainability & Exit Strategy (+15 pts)
    dim11_score = 0
    if re.search(r'sustainability plan|exit strategy|revenue diversification|step-down funding|transition plan', text, re.IGNORECASE):
        dim11_score += 15
    respond_score += min(dim11_score, 15)

    # Dimension 12: Submission Infrastructure (+15 pts)
    dim12_score = 0
    if re.search(r'grants\.gov|era commons|aor registration|electronic signature|pdf specifications', text, re.IGNORECASE):
        dim12_score += 15
    respond_score += min(dim12_score, 15)

    # Dimension 13: Program Design & Evaluation (+15 pts)
    dim13_score = 0
    if re.search(r'methodology section|research design|baseline data plan|comparison group|statistical analysis|external evaluator', text, re.IGNORECASE):
        dim13_score += 15
    respond_score += min(dim13_score, 15)

    # --- Final Classification ---
    if respond_score >= 60:
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
