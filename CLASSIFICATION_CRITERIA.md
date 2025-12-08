# Grant Proposal Classification System Documentation

## Executive Summary
This document defines the architectural logic for the **Grant Proposal Classification System**. The system autonomously routes incoming proposal documents into one of two processing workflows: **Respond (Type 1)** or **Flex (Type 2)**.

The distinction is fundamental to the downstream automation strategy:
*   **Respond (Type 1)** documents are **Transactional**, requiring high-precision data extraction from rigid templates.
*   **Flex (Type 2)** documents are **Generative**, requiring large language models to synthesize narratives from unstructured prompts.

This classification framework minimizes processing errors by ensuring the correct "worker" (extractor vs. writer) is assigned to the task.

---

## Part 1: Comparative Analysis by Dimension

### Dimension 1: Application Structure & Gating
| Attribute | Respond (Type 1) | Flex (Type 2) |
| :--- | :--- | :--- |
| **Format** | Rigid, pre-defined templates (PDF Forms, Word Tables). | Open-ended documents (RFPs, Question Lists). |
| **Gating** | Hard gates (boxes, character limits). | Soft gates (page limits, word count guidelines). |
| **Segmentation** | Explicitly segmented (Chapter 1, Appendix A). | Flowing or hierarchical (Headings, Paragraphs). |

### Dimension 2: Context Dependence
*   **Respond (Type 1):** **Low Context.** Answers are often isolated facts (e.g., "Organization Name," "Total Budget"). Field A does not necessarily inform Field B.
*   **Flex (Type 2):** **High Context.** Answers are interconnected. The "Problem Statement" creates the logical foundation for the "Proposed Solution." The writing must maintain a cohesive narrative arc.

### Dimension 3: Writing Effort & Volume
*   **Respond (Type 1):** **Low/Moderate Effort.** Focus is on retrieval and entry of existing data. High volume of short fields.
*   **Flex (Type 2):** **High Effort.** Focus is on synthesis and persuasion. Lower volume of "fields," but significantly higher volume of generated text per response.

### Dimension 4: Budget Complexity & Justification
*   **Respond (Type 1):** Tabular data entry. "Fill in the rows for Personnel, Supplies, Travel."
*   **Flex (Type 2):** Narrative justification. "Explain why the travel budget is necessary to achieve the program goals."

### Dimension 5: Supporting Documents & Credential Requirements
*   **Respond (Type 1):** Checklists. "Attach IRS Letter," "Attach Board List." The system just needs to verify presence.
*   **Flex (Type 2):** Integration. " Incorporate the findings of your last audit into the organizational capacity section."

---

## Part 2: Routing Logic Framework

The routing decision is a binary classification problem executed by the AI Router.

1.  **Input:** Document File (PDF/DOCX) -> Text Extraction (First 10 Pages/50 Paragraphs).
2.  **Analysis:** The AI evaluates the text against the **Evidence Summary Matrix** (Part 3).
3.  **Decision:**
    *   **IF** `Signal_Score(Respond) > Signal_Score(Flex)` **THEN** Route to **Extraction Pipeline**.
    *   **IF** `Signal_Score(Flex) > Signal_Score(Respond)` **THEN** Route to **Narrative Generation Pipeline**.

---

## Part 3: Evidence Summary Matrix

| Indicator | Signal for **Respond (Type 1)** | Signal for **Flex (Type 2)** |
| :--- | :--- | :--- |
| **Keywords** | "Form," "Template," "Checklist," "Fill-in," "Chapter," "Appendix" | "RFP," "Request for Proposal," "Guidelines," "Narrative," "Questions" |
| **Visuals** | Empty boxes, underscores (`_____`), grid lines, checkboxes. | Bulleted lists of questions, long paragraphs of instructions. |
| **Instructions** | "Do not exceed space," "Select one," "Attached is the form." | "Describe," "Explain," "Submit a proposal not exceeding 5 pages." |
| **Metadata** | File names like `Form_1023.pdf`, `App_Template.docx`. | File names like `2025_Guidelines.pdf`, `Program_RFP.pdf`. |

---

## Part 4: Implementation Specification

The current implementation utilizes a Python-based script (`classify_proposals.py`) acting as the Router.

*   **Language:** Python 3.8+
*   **Core Libraries:**
    *   `pypdf`: For PDF text extraction.
    *   `python-docx`: For Word document text extraction.
    *   `google-generativeai`: Interface for the LLM decision engine.
*   **Model:** Google Gemini 2.5 Pro.
*   **Input Handling:**
    *   Accepts multiple file paths as command-line arguments.
    *   Extracts a representative text snippet (Header + First 10 pages) to minimize token usage while maximizing context.
*   **Output Schema:**
    *   JSON Object mapping `filepath` to `classification` and `reasoning`.

---

## Part 5: Outliers & Edge Cases

1.  **Hybrid Documents:**
    *   *Scenario:* An RFP (Flex) that contains a small form (Respond) at the end.
    *   *Policy:* Classify as **Flex (Type 2)**. The primary task is the narrative generation; the form is a sub-task.
2.  **Empty Templates:**
    *   *Scenario:* A file containing only headers and no content.
    *   *Policy:* Classify based on *intent* inferred from headers. If headers ask for "Name/Address" -> **Respond**. If headers ask "Project Description" -> **Flex**.
3.  **Ambiguous Instructions:**
    *   *Scenario:* "Please provide your details below" followed by 5 blank pages.
    *   *Policy:* Defaults to **Flex (Type 2)** to ensure a human or high-level AI reviews the writing requirement, avoiding data extraction failure.

---

## Part 6: Prompt Engineering for Router AI

The following prompt structure is injected into the Gemini model to enforce the logic defined above:

```text
Analyze the following text extracted from a grant proposal document.
Classify it into one of two types based on these definitions:

1. **Respond (Type 1)**: Structured forms, fill-in-the-blank templates, applications with rigid segmentation...
2. **Flex (Type 2)**: Unstructured narratives, Request for Proposals (RFP), guidelines, question lists...

Filename: {filename}

Text Snippet:
{text_snippet}

Return a valid JSON object with exactly two keys:
- "classification": "Flex (Type 2)" or "Respond (Type 1)"
- "reasoning": A brief explanation of why this classification was chosen.
```

*Key Prompting Features:*
*   **Definition Injection:** Explicitly defining the types reduces hallucination.
*   **Filename Context:** Providing the filename helps resolve ambiguity (e.g., `Template.pdf` vs `Guidelines.pdf`).
*   **Structured Output:** Enforcing JSON ensures programmatic parsability.

---

## Part 7: Validation & Confidence Intervals

Validation of the classification is performed by reviewing the `reasoning` field in the JSON output.

*   **High Confidence:** The reasoning cites specific keywords ("Found 'Application Form' in header") or structural elements ("Detected multiple fillable fields").
*   **Low Confidence:** The reasoning is vague ("Looks like a document") or cites conflicting evidence ("Contains both form fields and narrative questions").

*Recommendation:* For production systems, flag classifications where the `reasoning` text length is short (< 20 chars) or ambiguous for manual review.
