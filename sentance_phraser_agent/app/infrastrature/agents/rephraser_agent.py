from pathlib import Path
import json

from ..llm.llm_factory import llm
from ..prompts.get_sentance_rephraser_prompt import SENTANCE_REPHRASER_AGENT_GENERATION_PROMPT
from ...utils.token_usage import extract_token_usage

BASE_DIR = Path(__file__).resolve().parent.parent / "prompts"


CONSTITUTION = (
    BASE_DIR / "sentance_rephraser_agent_input_files" / "constitution.md"
).read_text(encoding="utf-8")

SPECIFICATION = (
    BASE_DIR / "sentance_rephraser_agent_input_files" / "specification.md"
).read_text(encoding="utf-8")

SYSTEM_PROMPT = (
    BASE_DIR / "sentance_rephraser_agent_input_files" / "system_prompt.md"
).read_text(encoding="utf-8")


async def rephraser_agent(content: str) -> dict:
    chain = SENTANCE_REPHRASER_AGENT_GENERATION_PROMPT | llm

    response = await chain.ainvoke(
        {
            "constitution": CONSTITUTION,
            "specification": SPECIFICATION,
            "user_prompt": SYSTEM_PROMPT,
            "content": content,
        }
    )

    return {
        "data": json.loads(response.content),
        "token_usage": extract_token_usage(response),
    }
