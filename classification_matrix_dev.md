# Developer Classification Matrix

This document provides a technical, at-a-glance summary of the classification logic implemented in `classify_proposals.py`.

## 1. Final Score Calculation

The final classification is determined by a `final_score` calculated as follows:

1.  **Text Separation**: The document text is separated into `instruction_text` and `question_text` using a keyword-based heuristic.
2.  **Complexity Scores**: A `calculate_complexity_score` function is called on each text component to produce an `instruction_score` and a `question_score`.
3.  **Weighted Average**: The initial `final_score` is a weighted average: `(instruction_score * 0.6) + (question_score * 0.4)`.
4.  **Gap Score Adjustment**: A `gap_score` (`instruction_score - question_score`) is calculated.
    - If `15 <= gap_score <= 30`, `final_score += 10`.
    - If `gap_score > 30`, `final_score += 20`.
5.  **Classification**:
    - If `final_score >= 60`, the document is classified as **RESPOND**.
    - Otherwise, it is classified as **FLEX**.

## 2. Hard Switch Rules (Applied Before Scoring)

These rules automatically classify a document, bypassing the scoring logic entirely.

### Automatic RESPOND Classification

| Condition | Logic |
|---|---|
| **Filename-Based** | `re.search(r'chapter\|appendix', filename, re.IGNORECASE)` |
| **Complex LOI** | `re.search(r'letter of inquiry\|loi', text)` AND (`num_pages > 3` OR `re.search(r'methods\|literature', text)`) |
| **Budget Form** | `re.search(r'budget justification form', text)` |
| **Federal Systems** | `re.search(r'grants\.gov\|era commons\|study section\|quarterly reporting', text)` |
| **Formal Frameworks**| `re.search(r'theory of change required\|capacity assessment.*scoring', text)` |

### Automatic FLEX Classification

| Condition | Logic |
|---|---|
| **Simple Submission**| `num_pages <= 3` AND `re.search(r'email submission', text)` AND `re.search(r'any format', text)` |
| **Community Review**| `re.search(r'community review', text)` |
| **Simple Reporting**| `re.search(r'annual or final report only', text)` |

## 3. Complexity Scoring (`calculate_complexity_score` function)

This function calculates a complexity score for a given block of text.

### Supplemental Heuristics

| Heuristic | Points | Keywords |
|---|---|---|
| **Filename Clues** | +15 | `cover page`, `exe statement` |
| **Doc Structure** | +10 | `table of contents`, `list of figures` |
| **Bureaucracy** | +15 | `certification`, `ordinance`, `executive order`, `cfr`, `debarment`, `assessed valuation`, `obligation bond` |

### 13 Dimensions of Scoring

| # | Dimension | Max Pts | Keywords & Logic |
|---|---|---|---|
| 1 | **Structure** | 25 | `num_pages > 15` (+15), `loi`, `invitation required`, `separate budget justification` (+10), `background`+`methods`+`budget` (+5) |
| 2 | **Evidence** | 20 | `literature review`, `references`, `current scholarship`, `evidence base`, `irb approval`, `ethics review` |
| 3 | **Volume** | 15 | `len(text.split()) > 6000` (+10), `methodology section`, `research design`, `conceptual framework`, `indirect costs`, `salary cap` (+10) |
| 4 | **Specificity** | 15 | `rubric` (+10), >3 compound questions (e.g., `what...and...or`) (+10) |
| 5 | **Metrics** | 15 | `year-by-year projections`, `5-year cash flow`, `quantifiable metrics`, `cost per`, `cost-effectiveness` |
| 6 | **Review** | 15 | `study section`, `peer review`, `scientific expertise`, `reviewer qualifications`, `consensus scoring` |
| 7 | **Monitoring** | 20 | `ffr required`, `quarterly reporting`, `rppr`, `site visits`, `data safety monitoring`, `audit requirement`, `sam.gov` |
| 8 | **Capacity** | 15 | `capacity assessment`, `oca`, `scoring matrix`, `track record verification`, `staff credential check` |
| 9 | **Framework** | 15 | `theory of change`, `logic model`, `logframe`, `assumptions section`, `baseline data`, `comparison group` |
| 10| **Budget** | 15 | `cost-effectiveness`, `cost per`, `line-item justification`, `cost estimation methodology`, `market benchmarks` |
| 11| **Sustainability**| 15 | `sustainability plan`, `exit strategy`, `revenue diversification`, `step-down funding`, `transition plan` |
| 12| **Infrastructure**| 15 | `grants.gov`, `era commons`, `aor registration`, `electronic signature`, `pdf specifications` |
| 13| **Evaluation** | 15 | `methodology section`, `research design`, `baseline data plan`, `comparison group`, `statistical analysis` |
