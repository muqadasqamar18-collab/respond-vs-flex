# Condensed RESPOND vs FLEX Grant Classification Framework

## 1. Executive Summary

- **Core Insight**: RESPOND and FLEX represent two fundamentally different funding philosophies.
  - **RESPOND** = Barrier Architecture (filters for sophisticated applicants).
  - **FLEX** = Barrier Removal (opens doors to under-resourced organizations).
- **Decision Threshold**:
  - **RESPOND Score ≥ 60 points** → Route to RESPOND AI
  - **RESPOND Score < 60 points** → Route to FLEX AI

## 2. Philosophy Comparison

| Aspect | RESPOND Philosophy | FLEX Philosophy |
|---|---|---|
| **Risk Management** | Gating and monitoring | Relationship and feedback |
| **Expertise Assumption**| "We have the expertise" | "Communities have the expertise"|
| **Capacity Proof** | Prove capacity upfront | Demonstrate through delivery |
| **Investment Focus** | Evaluation infrastructure | Access and trust |
| **Typical Timeline** | 4-6 months + specialist team | 1-2 weeks + organizational knowledge|
| **Evidence Standards**| 75-95% external validation | 15-40% internal sufficient |

## 3. The 13 Dimensions of Classification

### Dimension 1: Application Structure & Gating (+25 pts)
- **Measures**: Structural complexity and number of "gates" an applicant must pass.
- **RESPOND**: Multi-stage, high-friction process.
  - **Keywords**: `LOI`, `invitation required`, `separate budget justification`, `Pre-Award Risk Assessment`, `labeled sections` (Background, Methods, Budget).
- **FLEX**: Single-stage, low-friction submission.

### Dimension 2: External Evidence Requirement (+20 pts)
- **Measures**: Reliance on external vs. internal knowledge.
- **RESPOND**: Externally anchored (60-95% external evidence).
  - **Keywords**: `literature review`, `references`, `current scholarship`, `evidence base`, `IRB approval`, `ethics review`.
- **FLEX**: Internal knowledge is sufficient.

### Dimension 3: Writing Effort & Volume (+15 pts)
- **Measures**: Total writing burden (word count, semantic density).
- **RESPOND**: Dense, technical (8k-18k words).
  - **Keywords**: `methodology section`, `research design`, `conceptual framework`, `indirect costs`, `salary cap`, `statistical power`.
- **FLEX**: Light, narrative (800-4k words).

### Dimension 4: Question Specificity (+15 pts)
- **Measures**: Whether questions are compound/technical or simple/plain-language.
- **RESPOND**: Compound, multi-step questions requiring specialized knowledge.
  - **Keywords**: Questions with `AND` / `but also`, `if/then` logic, references to external `rubric`.
- **FLEX**: Single-intent questions using plain language.

### Dimension 5: Demonstrable Outcomes & Metrics (+15 pts)
- **Measures**: Whether quantifiable metrics are mandatory or qualitative narratives are acceptable.
- **RESPOND**: Quantifiable metrics required.
  - **Keywords**: `year-by-year projections`, `5-year cash flow`, `quantifiable metrics`, `cost per`, `cost-effectiveness ratio`, `baseline data`.
- **FLEX**: Qualitative narrative is acceptable.

### Dimension 6: Reviewer Expertise (+15 pts)
- **Measures**: Whether review is by scientific experts or community/staff.
- **RESPOND**: Scientific expert peer review.
  - **Keywords**: `study section`, `peer review`, `scientific expertise`, `reviewer qualifications`, `consensus scoring`.
- **FLEX**: Community or organizational review.

### Dimension 7: Post-Award Monitoring (+20 pts)
- **Measures**: The ongoing compliance and reporting burden after funding.
- **RESPOND**: Continuous, multi-part reporting.
  - **Keywords**: `FFR required`, `quarterly reporting`, `RPPR`, `site visits`, `Data Safety Monitoring`, `audit requirement`, `SAM.gov`.
- **FLEX**: End-of-period reporting only.

### Dimension 8: Organizational Capacity Assessment (+15 pts)
- **Measures**: Whether formal capacity assessment is a pre-award gate.
- **RESPOND**: Formal capacity assessment required.
  - **Keywords**: `capacity assessment`, `OCA`, `scoring matrix`, `track record verification`, `staff credential check`, `risk rating`.
- **FLEX**: No formal capacity assessment.

### Dimension 9: Evidence Framework (+15 pts)
- **Measures**: Whether formal causal frameworks (Theory of Change, Logic Models) are required.
- **RESPOND**: Formal logic mapping required.
  - **Keywords**: `theory of change`, `logic model`, `logframe`, `assumptions section`, `baseline data`, `comparison group`.
- **FLEX**: Narrative logic is acceptable.

### Dimension 10: Budget Justification (+15 pts)
- **Measures**: Level of detail required for budget and cost analysis.
- **RESPOND**: Line-item justification and cost-effectiveness rigor.
  - **Keywords**: `cost-effectiveness`, `cost per`, `line-item justification`, `cost estimation methodology`, `market benchmarks`, `indirect rate`, `NICRA`.
- **FLEX**: Simple budget summaries.

### Dimension 11: Sustainability & Exit Strategy (+15 pts)
- **Measures**: Whether a formal sustainability plan is required.
- **RESPOND**: Formal sustainability planning required.
  - **Keywords**: `sustainability plan`, `exit strategy`, `revenue diversification`, `step-down funding`, `transition plan`.
- **FLEX**: Implicit or brief sustainability description.

### Dimension 12: Submission Infrastructure (+15 pts)
- **Measures**: Technical complexity of submission systems.
- **RESPOND**: Complex, formal infrastructure.
  - **Keywords**: `Grants.gov`, `eRA Commons`, `AOR registration`, `electronic signature`, `PDF specifications`.
- **FLEX**: Simple, accessible submission.

### Dimension 13: Program Design & Evaluation (+15 pts)
- **Measures**: Rigor of methodology and evaluation sections.
- **RESPOND**: Formal methodology and rigorous evaluation.
  - **Keywords**: `methodology section`, `research design`, `baseline data plan`, `comparison group`, `statistical analysis`, `external evaluator`.
- **FLEX**: Flexible, community-defined evaluation.

## 4. Supplemental Heuristics (for ambiguous documents)

- **Filename Analysis (+15 pts)**: Filenames containing terms like `chapter`, `appendix`, `cover page`, or `exe statement` are strong indicators of a larger, more complex `RESPOND` document.
- **Document Structure Analysis (+10 pts)**: The presence of a `table of contents` or `list of figures` suggests a formal, structured document typical of `RESPOND` grants.
- **Bureaucratic Complexity (+15 pts)**: Keywords related to legal, financial, and regulatory compliance (e.g., `certification`, `ordinance`, `executive order`, `CFR`, `debarment`, `assessed valuation`, `obligation bond`) are strong signals of a `RESPOND` grant.

## 5. Hard Switch Rules (Automatic Classification)

### Automatic RESPOND If:
- Document requires `LOI` and is complex (>3 pages, mentions `methods` or `literature`).
- Requires separate `budget justification form`.
- Mentions `Grants.gov`, `eRA Commons`, `study section`, or `quarterly reporting`.
- Requires a formal `theory of change` or `capacity assessment` with scoring.

### Automatic FLEX If:
- Document is < 8 pages, has simple narrative prompts, and no mention of `budget justification`, `methodology`, or `IRB`.
- Submission is via `email` and `any format` is accepted.
- Review process is explicitly `community review`.
- Reporting is `annual or final report only`.
