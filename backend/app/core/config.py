import os
from typing import Tuple
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

# Pre-load environment variables from .env into system memory
load_dotenv()

class Settings(BaseModel):
    # GENERAL CONFIGURATIONS
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Hermes Engineering Crew")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # SHARED AI BACKBONE ROUTING
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")

    # CORE AGENT MODEL SELECTION
    WORKER_MODEL: str = os.getenv("WORKER_MODEL", "gemma3:1b")
    MASTER_MODEL: str = os.getenv("MASTER_MODEL", "hermes3:3b")

    # TIMEOUT BOUNDARIES (Synced to 10-minute maximum safety windows)
    WORKER_TIMEOUT: int = int(os.getenv("WORKER_TIMEOUT", 600))
    MASTER_TIMEOUT: int = int(os.getenv("MASTER_TIMEOUT", 600))
    GITHUB_FETCH_TIMEOUT: int = int(os.getenv("GITHUB_FETCH_TIMEOUT", 600))

    # REGULATED INGESTION DATA RESTRICTIONS
    MAX_REPO_FILES: int = int(os.getenv("MAX_REPO_FILES", 8))
    MAX_FILE_CONTENT_LENGTH: int = int(os.getenv("MAX_FILE_CONTENT_LENGTH", 800))
    
    # FILE EXTENSION TRACKING
    SUPPORTED_EXTENSIONS: Tuple[str, ...] = (
        os.getenv("SUPPORTED_EXTENSIONS", ".py,.js,.ts,.tsx,.jsx,.php,.go,.java,.rs,.md")
    )

    # ⚡ FIELD VALIDATOR (Converts comma-separated string into an immutable tuple object)
    @field_validator("SUPPORTED_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        if isinstance(v, str):
            return tuple(ext.strip() for ext in v.split(",") if ext.strip())
        return tuple(v)

# Instantiate the structured system settings map object
settings = Settings()