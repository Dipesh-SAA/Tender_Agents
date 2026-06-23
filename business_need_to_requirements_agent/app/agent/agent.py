from pathlib import Path

from langchain_core.output_parsers import JsonOutputParser

from business_need_to_requirements_agent.app.Infrastrature.llm.llm_factory import get_llm
from business_need_to_requirements_agent.app.Infrastrature.prompts.prompt import REQUIREMENT_GENERATION_PROMPT


BASE_DIR = Path(__file__).resolve().parent.parent / "Infrastrature"

CONSTITUTION = (
    BASE_DIR / "input_files" / "constitution.md"
).read_text(encoding="utf-8")

SPECIFICATION = (
    BASE_DIR / "input_files" / "specification.md"
).read_text(encoding="utf-8")

USER_PROMPT = (
    BASE_DIR / "input_files" / "user_prompt.md"
).read_text(encoding="utf-8")


def generate_requirements(
    requirement_input: dict,
    provider: str | None = None,
) -> dict:
    """
    Generate Business Requirements,
    Functional Requirements,
    Non Functional Requirements,
    Data Requirements,
    Integration Requirements
    from Canonical Requirements.
    """

    canonical_requirements = (
        requirement_input.get(
            "CanonicalRequirements",
            []
        )
    )

    if not canonical_requirements:
        raise ValueError(
            "CanonicalRequirements cannot be empty"
        )

    llm = get_llm(provider)

    chain = (
        REQUIREMENT_GENERATION_PROMPT
        | llm
        | JsonOutputParser()
    )

    response = chain.invoke(
        {
            "constitution": CONSTITUTION,
            "specification": SPECIFICATION,
            "user_prompt": USER_PROMPT,

            "TenderId":
                requirement_input.get(
                    "TenderId",
                    ""
                ),

            "CompanyId":
                requirement_input.get(
                    "CompanyId",
                    ""
                ),

            "RequirementDeduplicationId":
                requirement_input.get(
                    "RequirementDeduplicationId",
                    ""
                ),

            "RequirementExtractionId":
                requirement_input.get(
                    "RequirementExtractionId",
                    ""
                ),

            "UploadedFileId":
                requirement_input.get(
                    "UploadedFileId",
                    ""
                ),

            "RawRequirementCount":
                requirement_input.get(
                    "RawRequirementCount",
                    0
                ),

            "CanonicalRequirementCount":
                requirement_input.get(
                    "CanonicalRequirementCount",
                    0
                ),

            "DuplicateRemovedCount":
                requirement_input.get(
                    "DuplicateRemovedCount",
                    0
                ),

            "CanonicalRequirements":
                canonical_requirements,

            "output_mode":
                "json_only"
        }
    )

    return response
