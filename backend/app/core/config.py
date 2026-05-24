import os
from typing import Tuple
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

load_dotenv()


class Settings:

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Hermes Engineering Crew")
    
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
    
    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )
    
    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )

    WORKER_MODEL = os.getenv(
        "WORKER_MODEL",
        "gemma3:1b"
    )
    MASTER_MODEL = os.getenv(
        "MASTER_MODEL",
        "hermes3:3b"
    )

    WORKER_TIMEOUT = int(
        os.getenv("WORKER_TIMEOUT", 300)
    )

    MAX_REPO_FILES = int(
        os.getenv("MAX_REPO_FILES", 8)
    )

    MAX_FILE_CONTENT_LENGTH = int(
        os.getenv(
            "MAX_FILE_CONTENT_LENGTH",
            800
        )
    )
    
    # Define it as a tuple of strings
    SUPPORTED_EXTENSIONS: Tuple[str, ...] = (".py", ".js", ".ts") # Fallback defaults

    @field_validator("SUPPORTED_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        if isinstance(v, str):
            # Split by comma and strip out any accidental spaces
            return tuple(ext.strip() for ext in v.split(",") if ext.strip())
        return tuple(v)


settings = Settings()