from fastapi import FastAPI
from business_need_to_requirements_agent.app.api.router.router import router

app = FastAPI(
    title="Requirement Generation Agent"
)

app.include_router(router)
