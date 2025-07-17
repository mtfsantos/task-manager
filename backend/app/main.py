import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.api.endpoints import tasks, auth
from app.core.logging_config import setup_logging # New import for logging setup

# Configure logging at the start
setup_logging()
logger = logging.getLogger(__name__) # Get logger instance after setup

# Define lifespan events for the application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup: No longer calling Base.metadata.create_all() here.
    # Alembic will manage database schema.
    logger.info("Application starting up. Database schema managed by Alembic.") # Updated log message
    yield
    # On shutdown: Perform any cleanup if necessary
    logger.info("Application shutdown completed.")


app = FastAPI(
    title="Task Management API",
    description="API for managing tasks, including creation, listing, filtering, updating, and deletion.",
    version="1.0.0",
    lifespan=lifespan # Link the lifespan manager
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
app.include_router(auth.router, prefix="/api/v1", tags=["authentication"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Task Management API!"}
