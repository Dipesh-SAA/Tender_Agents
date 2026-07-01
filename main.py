from fastapi import FastAPI
from business_need_to_requirements_agent.app.api.router.router import router
from fastapi.middleware.cors import CORSMiddleware
from sentance_phraser_agent.app.api.router.routes import router as grammar_router

app = FastAPI(
    title="Tender Agents API",
    description="API for requirement generation, grammar correction, and sentence rephrasing",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(grammar_router)
app.include_router(router)


@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": "Tender Agents API",
        "version": "1.0.0",
    }
