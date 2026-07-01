from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import time
import uuid
from ...infrastrature.agents.rephraser_agent import rephraser_agent
from ...utils.logger import AgentLogger
# Import your async LLM task
from ...infrastrature.agents.grammer_agent import grammer_agent

router = APIRouter(
    prefix="/grammar",
    tags=["Grammar Correction"]
)

logger = AgentLogger()


class RequestBody(BaseModel):
    content: str


@router.post("/grammer_correction")
async def grammar_correction_api(
    request: RequestBody
):
    start_time = time.perf_counter()
    correlation_id = str(uuid.uuid4())
    agent_name = "GrammarCorrectionAgent"
    source_module = "api.router.router"

    try:
        logger.log_event(
            agent_name=agent_name,
            message="Grammar correction process started",
            event_type="REQUEST_RECEIVED",
            source_module=source_module,
            is_success=True,
            correlation_id=correlation_id,
            payload=request.model_dump()
        )

        # ==========================
        # RUN LLM AGENT TASK
        # ==========================
        agent_response = await grammer_agent(content=request.content)
        

        logger.log_event(
            agent_name=agent_name,
            message="Grammar corrected successfully via LLM",
            event_type="AGENT_COMPLETED",
            source_module=source_module,
            is_success=True,
            correlation_id=correlation_id
        )

        duration_ms = int((time.perf_counter() - start_time) * 1000)

        logger.log_event(
            agent_name=agent_name,
            message="Grammar correction completed successfully",
            event_type="OUTPUT_SAVED",
            source_module=source_module,
            is_success=True,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            payload={
                "content_length": len(request.content),
                "token_usage": agent_response["token_usage"],
            }
        )

        return {
            "success": True,
            "data": agent_response["data"],
            "token_usage": agent_response["token_usage"],
        }

    except Exception as ex:
        duration_ms = int((time.perf_counter() - start_time) * 1000)

        logger.log_event(
            agent_name=agent_name,
            message=str(ex),
            event_type="ERROR",
            source_module=source_module,
            is_success=False,      
            duration_ms=duration_ms,
            correlation_id=correlation_id
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )
    






@router.post("/sentence_rephrase")
async def sentence_rephraser_api(
    request: RequestBody
):
    start_time = time.perf_counter()
    correlation_id = str(uuid.uuid4())
    agent_name = "SentenceRephraserAgent"
    source_module = "api.router.router"

    try:
        logger.log_event(
            agent_name=agent_name,
            message="Sentence rephrasing process started",
            event_type="REQUEST_RECEIVED",
            source_module=source_module,
            is_success=True,
            correlation_id=correlation_id,
            payload=request.model_dump()
        )

        # ==========================
        # RUN LLM AGENT TASK
        # ==========================
        agent_response = await rephraser_agent(
            content=request.content
        )

        logger.log_event(
            agent_name=agent_name,
            message="Sentence rephrased successfully via LLM",
            event_type="AGENT_COMPLETED",
            source_module=source_module,
            is_success=True,
            correlation_id=correlation_id
        )

        duration_ms = int((time.perf_counter() - start_time) * 1000)

        logger.log_event(
            agent_name=agent_name,
            message="Sentence rephrasing completed successfully",
            event_type="OUTPUT_SAVED",
            source_module=source_module,
            is_success=True,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            payload={
                "content_length": len(request.content),
                "token_usage": agent_response["token_usage"],
            }
        )

        return {
            "success": True,
            "data": agent_response["data"],
            "token_usage": agent_response["token_usage"],
        }

    except Exception as ex:
        duration_ms = int((time.perf_counter() - start_time) * 1000)

        logger.log_event(
            agent_name=agent_name,
            message=str(ex),
            event_type="ERROR",
            source_module=source_module,
            is_success=False,
            duration_ms=duration_ms,
            correlation_id=correlation_id
        )

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )
