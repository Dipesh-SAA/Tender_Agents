from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import time
import uuid

from business_need_to_requirements_agent.app.agent.agent import generate_requirements
from business_need_to_requirements_agent.app.services.mongo.mongo_services import MongoServices
from business_need_to_requirements_agent.app.utils.logger import AgentLogger


router = APIRouter(
    prefix="/requirements",
    tags=["Requirement Generation"]
)

logger = AgentLogger()


class RequirementGenerationRequest(BaseModel):
    tender_id: str
    company_id: str



@router.post("/generate")
async def generate_requirement_output(
    request: RequirementGenerationRequest
):

    start_time = time.perf_counter()

    correlation_id = str(uuid.uuid4())

    agent_name = "RequirementGenerationAgent"

    source_module = (
        "api.router.router"
    )

    try:

        logger.log_event(
            agent_name=agent_name,
            message="Requirement generation started",
            event_type="REQUEST_RECEIVED",
            source_module=source_module,
            is_success=True,
            correlation_id=correlation_id,
            payload=request.model_dump()
        )

        mongo_service = MongoServices()

        # ==========================
        # FETCH INPUT FROM MONGO
        # ==========================

        input_data = (
            mongo_service.get_requirement_input(
                tender_id=request.tender_id,
                company_id=request.company_id
            )
        )

        logger.log_event(
            agent_name=agent_name,
            message="Requirement input loaded",
            event_type="INPUT_LOADED",
            source_module=source_module,
            is_success=True,
            correlation_id=correlation_id,
            payload={
                "TenderId": request.tender_id,
                "CompanyId": request.company_id,
                "CanonicalRequirementCount":
                    input_data.get(
                        "CanonicalRequirementCount",
                        0
                    )
            }
        )

        # ==========================
        # RUN AGENT
        # ==========================

        response = generate_requirements(
            requirement_input=input_data,
        )

        logger.log_event(
            agent_name=agent_name,
            message="Requirements generated successfully",
            event_type="AGENT_COMPLETED",
            source_module=source_module,
            is_success=True,
            correlation_id=correlation_id
        )

        # ==========================
        # SAVE OUTPUT
        # ==========================

        mongo_service.save_requirements(
            tender_id=request.tender_id,
            company_id=request.company_id,
            requirement_deduplication_id=
                input_data[
                    "RequirementDeduplicationId"
                ],
            output_json=response
        )

        duration_ms = int(
            (
                time.perf_counter()
                - start_time
            ) * 1000
        )

        logger.log_event(
            agent_name=agent_name,
            message="Requirements saved successfully",
            event_type="OUTPUT_SAVED",
            source_module=source_module,
            is_success=True,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            payload={
                "TenderId": request.tender_id,
                "CompanyId": request.company_id
            }
        )

        return {
            "success": True,
            "message": "Requirements generated successfully",
            "correlation_id": correlation_id,
            "duration_ms": duration_ms,
            "data": response
        }

    except Exception as ex:

        duration_ms = int(
            (
                time.perf_counter()
                - start_time
            ) * 1000
        )

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
