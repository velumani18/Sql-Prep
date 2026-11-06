from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.sql import router as sql_router
from app.api.databases import router as databases_router
from app.api.questions import router as questions_router
from app.api.curriculum import router as curriculum_router
from app.api.auth import router as auth_router
from app.api.progress import router as progress_router
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Interactive SQL Execution Sandbox and Semantic Evaluation Engine",
)

# Enable CORS for local Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(auth_router)
app.include_router(curriculum_router)
app.include_router(questions_router)
app.include_router(databases_router)
app.include_router(sql_router)
app.include_router(progress_router)


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
    }


@app.get("/", tags=["System"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs_url": "/docs",
    }
