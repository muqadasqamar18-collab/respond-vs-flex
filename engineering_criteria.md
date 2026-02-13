### Subjective vs. Objective Criteria

#### Subjective Criteria (Requires NLP/LLM Interpretation)

These criteria require a model that can understand the semantic meaning and intent of the text.

1.  **Writing Style: Technical vs. Narrative**
    *   **Respond (Complex):** The document uses formal, technical language. It might include jargon related to research methodologies (e.g., "quantitative analysis," "statistical power"), finance (e.g., "fiduciary responsibility," "audited statements"), or legal compliance (e.g., "procurement rules," "indemnification").
    *   **Reflex (Simple):** The document encourages persuasive, narrative writing. It uses words like "story," "narrative," "compelling case," or asks for the organization's "mission and vision."

2.  **Prompt Complexity: Multi-Layered vs. Singular**
    *   **Respond (Complex):** Questions are often multi-part, requiring the applicant to address several distinct points within a single response. For example: "Describe your project's goals, how you will measure success, and what risks you've identified."
    *   **Reflex (Simple):** Questions are direct, singular, and ask for a specific piece of information. For example: "What is the title of your project?" or "Summarize your request in one sentence."

3.  **Answer Source: Document-Based vs. Creative**
    *   **Respond (Complex):** The answers must be tightly aligned with specific frameworks, rubrics, or evaluation criteria laid out *within the document itself*. The user has to constantly refer back to the document's rules to formulate an answer.
    *   **Reflex (Simple):** The answers are more creative and self-contained, relying on the user's own knowledge and storytelling ability rather than strict adherence to a complex set of rules in the prompt.

#### Objective Criteria (Can be Implemented with Code/Heuristics)

These criteria can be detected programmatically with a high degree of accuracy.

1.  **Length and Volume Indicators**
    *   **Respond (Complex):**
        *   The document explicitly requests a long-form response with a high page count (e.g., "a proposal of no more than 25 pages").
        *   It requires multiple, distinct supporting documents like a "Project Workplan," "Budget Justification," "Personnel Resumes," or "Financial Statements."
    *   **Reflex (Simple):**
        *   The document enforces brevity through strict character or word limits on key questions (e.g., "in 2,500 characters or less").
        *   It asks for simple attachments, like a list of board members or a standard organizational budget.

2.  **Presence of Keyword Categories**
    *   **Respond (Complex):** The document contains a high density of keywords from technical domains:
        *   **Research:** `quantitative`, `qualitative`, `statistical`, `methodology`, `hypothesis`, `peer review`
        *   **Finance:** `fiduciary`, `audit`, `financial statements`, `budget justification`, `liquidity`
        *   **Legal/Compliance:** `procurement`, `indemnification`, `liability`, `compliance`, `derogations`
    *   **Reflex (Simple):** The document contains keywords related to narrative and mission:
        *   **Narrative:** `story`, `mission`, `vision`, `narrative`, `community`, `impact`, `goals`

3.  **Structural Elements**
    *   **Respond (Complex):** The document contains sections titled "Evaluation Criteria," "Review Process," "Scoring Rubric," or similar, and these sections are detailed and multi-staged.
    *   **Reflex (Simple):** The application is a straightforward form with sections like "About Your Organization," "Project Description," and "Attachments."