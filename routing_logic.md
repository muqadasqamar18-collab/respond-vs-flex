# Part 2: The Routing Logic (The Criteria)

## Complexity Scorecard

The routing algorithm will assign a "Complexity Score" to each uploaded document based on the following rules. The final score will determine whether the document is routed to the "Respond" or "Flex" agent.

### Scoring System

*   **+3 points:** Strong indicators of high complexity.
*   **+1 point:** Moderate indicators of high complexity.
*   **-1 point:** Indicators of low complexity.

### Routing Thresholds

*   **Score > 5:** Route to **Respond**
*   **Score <= 5:** Route to **Flex**

### Scoring Rules

| Category                  | Rule                                                                                                                              | Points | Evidence                                                                                                                                                                                                                                                                                            |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Writing Effort & Volume** | Document requests a "proposal narrative" or "workplan" exceeding 10 pages.                                                       | +3     | In "2025-Application-Guide-Research-Grants-on-RI (1).pdf", the requirement is for a "proposal narrative of about 25 pages."                                                                                                                                                                     |
|                           | Document requires a "budget justification" or "personnel information."                                                               | +1     | In "Endowment-forHealth-Program-Grant-TI-ApplicationTemplate.docx", the applicant must provide a "Project Workplan," "Budget Justification," and "Personnel Information."                                                                                                                  |
|                           | Document imposes a character limit of less than 3,000 characters for a key descriptive section.                                      | -1     | In "2025SmallGrantQuestionList.pdf", the application imposes a "Character Limit: 2,500 characters including spaces."                                                                                                                                                                             |
| **Context Dependence**    | Document provides a detailed "evaluation criteria" or "review process" section.                                                  | +3     | In "2025-Application-Guide-Research-Grants-on-RI (1).pdf", the "Application Review Process" is a multi-stage, 10-15 month process.                                                                                                                                                            |
|                           | Document requires the applicant to select from a predefined framework, such as a "System Change Approach."                         | +1     | In "Endowment-forHealth-Program-Grant-TI-ApplicationTemplate.docx", the applicant must select from a predefined "System Change Approach" and then report on specific, corresponding "Goals and Measures."                                                                                     |
|                           | Document asks for the organization's "mission statement" or "vision."                                                               | -1     | In "2025 EXAMPLE Grant Application (1) (1).pdf", the application asks, "What is your mission statement?"                                                                                                                                                                                          |
| **Technical vs. Creative**  | Document uses technical terms like "quantitative," "qualitative," "statistical power," "fiduciary," or "procurement."               | +3     | In "2025-Application-Guide-Research-Grants-on-RI (1).pdf", the emphasis is on "rigorous methods" and "adequate statistical power." In "Application form for GPE grants.docx", terms like "fiduciary" and "procurement" are used.                                                          |
|                           | Document asks for a "narrative," "compelling case," or "story."                                                                    | -1     | In "2025 EXAMPLE Grant Application (1) (1).pdf", the instructions encourage a "clear and compelling case for funding."                                                                                                                                                                         |
| **Prompt Complexity**     | Document contains prompts with multiple, explicit sub-requirements.                                                               | +3     | In "Application form for GPE grants.docx", a single prompt asks the applicant to "describe how the proposed grant financing modality is evolving...," "Include what mechanisms are in place to mitigate fiduciary risks...," and "detail how the proposed program sets a foundation..." |
|                           | Document contains simple, single-part questions.                                                                                 | -1     | In "2025 EXAMPLE Grant Application (1) (1).pdf", the questions are direct and to the point, such as, "What is the title of the program/project?"                                                                                                                                                 |
