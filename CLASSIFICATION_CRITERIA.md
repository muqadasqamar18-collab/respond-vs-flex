# Grant Proposal Classification Criteria & Indicators

This document details the analytical framework used to distinguish between **Respond (Type 1)** and **Flex (Type 2)** grant proposals. The classification is not merely based on file format but on the *cognitive and structural demands* placed on the applicant.

## 1. Classification Matrix

| Feature | Respond (Type 1) | Flex (Type 2) |
| :--- | :--- | :--- |
| **Primary Task** | Data Entry / Form Filling | Narrative Generation / Composition |
| **Writing Effort** | Low to Moderate | High |
| **Technical Compliance** | High (Rigid Constraints) | Moderate (Structural Guidelines) |
| **Contextual Writing** | Low (Factual/Direct) | High (Persuasive/Storytelling) |
| **Document Structure** | Fixed (Templates, Boxes) | Open (Headings, Questions) |

---

## 2. Detailed Indicators

### A. Writing Effort
*   **Respond (Type 1):**
    *   **Indicator:** High frequency of short-answer fields, checkboxes, and drop-downs.
    *   **Effort Type:** "Transactional." The applicant provides existing data (e.g., EIN, Address, Budget Figures) or brief, constrained summaries.
    *   **Detection Signal:** Presence of "character limits" (often small, e.g., < 500 chars), "fillable" form fields, or rigid physical space on a page preventing expansion.

*   **Flex (Type 2):**
    *   **Indicator:** Requests for "Descriptions," "Narratives," "Approach," or "Strategy."
    *   **Effort Type:** "Generative." The applicant must synthesize information to create a cohesive argument or story. The length is often determined by page limits (e.g., "5 pages max") rather than character counts per field.
    *   **Detection Signal:** Terms like "Proposal Narrative," "Project Description," "Questions," or prompts that require multi-paragraph answers.

### B. Technical Compliance
*   **Respond (Type 1):**
    *   **Indicator:** Strict adherence to a pre-defined layout.
    *   **Compliance Factor:** The system expects data in specific locations for extraction. Deviating from the box invalidates the entry.
    *   **Detection Signal:** "Do not modify this form," "Use the space provided," segmented documents (e.g., "Chapter 3 only"), or file names indicating a specific part of a whole (e.g., "Appendix B").

*   **Flex (Type 2):**
    *   **Indicator:** Compliance is based on *content* coverage rather than *layout* rigidity.
    *   **Compliance Factor:** The applicant must ensure they answer all questions in a list, but they control the formatting, headers, and flow of the document (usually a Word doc or PDF export).
    *   **Detection Signal:** "RFP" (Request for Proposal), "Guidelines," "Question List," or instructions telling the applicant to "attach a narrative."

### C. Contextual Writing & Tone
*   **Respond (Type 1):**
    *   **Tone:** Objective, factual, concise.
    *   **Context:** Isolated. An answer in "Box A" usually stands alone and doesn't necessarily need to flow narratively into "Box B."
    *   **Keywords:** "Name," "Amount," "Date," "Select," "Check all that apply."

*   **Flex (Type 2):**
    *   **Tone:** Persuasive, holistic, connected.
    *   **Context:** Integrated. The "Problem Statement" must logically lead to the "Proposed Solution" and "Impact." The writing requires connecting dots between different sections.
    *   **Keywords:** "Describe," "Explain," "Justify," "Impact," "Sustainability," "Story."

### D. Visual & Structural Factors
*   **Respond (Type 1):**
    *   **Visuals:** Heavy use of tables, grid lines, gray background fields, and official headers/footers on every page.
    *   **Structure:** Linear and fragmented.
*   **Flex (Type 2):**
    *   **Visuals:** Text-heavy, paragraph structures, bullet points, potential for user-included images or charts.
    *   **Structure:** Hierarchical and flowing (Heading -> Subheading -> Paragraph).

---

## 3. Summary of Classification Logic

The AI classifier evaluates these dimensions to determine the document type:

1.  **If the document asks "What is X?"** -> likely **Respond (Type 1)**.
2.  **If the document asks "Why is X important and how will you achieve it?"** -> likely **Flex (Type 2)**.
