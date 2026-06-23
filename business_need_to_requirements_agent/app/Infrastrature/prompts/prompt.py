from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate


BASE_DIR = Path(__file__).resolve().parent.parent

CONSTITUTION = (
    BASE_DIR / "input_files" / "constitution.md"
).read_text(encoding="utf-8")

SPECIFICATION = (
    BASE_DIR / "input_files" / "specification.md"
).read_text(encoding="utf-8")

USER_PROMPT = (
    BASE_DIR / "input_files" / "user_prompt.md"
).read_text(encoding="utf-8")


REQUIREMENT_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert Tender Section Generator.

Follow the Constitution, Specification, and User Prompt exactly.

================ CONSTITUTION ================
{constitution}

================ SPECIFICATION ================
{specification}

================ USER PROMPT ================
{user_prompt}

Your responsibilities:

1. Generate a single proposal-ready section.
2. Use only supplied evidence and company context.
3. Never invent evidence.
4. Never invent certifications.
5. Never invent case studies.
6. Never invent project experience.
7. Never invent metrics or performance claims.
8. Return strictly specification-compliant JSON.
9. Do not return markdown.
10. Do not return explanations.
11. Do not return reasoning.
12. Do not return any text outside the JSON response.
"""
        ),
       (
    "human",
    """
TenderId:
{TenderId}

CompanyId:
{CompanyId}

RequirementDeduplicationId:
{RequirementDeduplicationId}

RequirementExtractionId:
{RequirementExtractionId}

UploadedFileId:
{UploadedFileId}

RawRequirementCount:
{RawRequirementCount}

CanonicalRequirementCount:
{CanonicalRequirementCount}

DuplicateRemovedCount:
{DuplicateRemovedCount}

CanonicalRequirements:
{CanonicalRequirements}

Generate:

1. Business Requirements
2. Functional Requirements
3. Non Functional Requirements
4. Data Requirements
5. Integration Requirements
6. Assumptions
7. Risks
8. Open Questions
9. Downstream Agent Handoff

Requirements must be derived only from the supplied
Canonical Requirements.

Maintain traceability to CanonicalRequirementId values.

Return only specification-compliant JSON.
"""
)

        ,
    ]
)
