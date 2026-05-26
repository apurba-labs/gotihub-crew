import httpx
import logging
from typing import Dict, Any, Union
from app.core.config import settings

logger = logging.getLogger("hermes.services.llm")

class LLMService:

    def __init__(self):
        # Fallback configs from core system settings
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.default_model = settings.WORKER_MODEL
        self.timeout = getattr(settings, "WORKER_TIMEOUT", 120.0)

    async def generate_response(self, payload: Union[str, Dict[str, Any]]) -> str:
        """
        Processes incoming agent requests. If given a dictionary, it routes straight 
        to /api/chat. If given a string, it routes cleanly to /api/generate.
        Optimized with hardware-level memory caching parameters to minimize latency.
        """
        # Define uniform local model execution optimizations
        optimized_options = {
            "num_ctx": 8192,         # 1. Expand context boundary limits to prevent cache thrashing
            "temperature": 0.2,      # 2. Lower temperature for faster, deterministic JSON layouts
            "num_predict": 3072,     # 3. Gives the sub-agents plenty of room to write detailed reports
            "use_mmap": True         # 4. Enforce memory-mapped files to guarantee instant KV caching
        }

        async with httpx.AsyncClient(timeout=float(self.timeout)) as client:
            try:
                # Scenario A: Agent sends a fully structured, production multi-turn dictionary payload
                if isinstance(payload, dict):
                    if "model" not in payload or not payload["model"]:
                        payload["model"] = self.default_model
                        
                    # Inject optimization options matrix if not explicitly defined by the caller
                    if "options" not in payload:
                        payload["options"] = optimized_options
                    else:
                        # Merge if options exist partially
                        payload["options"] = {**optimized_options, **payload["options"]}

                    target_url = f"{self.base_url}/api/chat"
                    logger.info(f"[LLMService] Routing CACHE-OPTIMIZED dictionary matrix to: {target_url}")
                    
                    response = await client.post(
                        target_url,
                        json=payload,
                        timeout=float(self.timeout)
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data["message"]["content"]

                # Scenario B: Legacy/Fallback single raw text prompt string handling
                else:
                    target_url = f"{self.base_url}/api/generate"
                    logger.info(f"[LLMService] Routing CACHE-OPTIMIZED flat prompt string to: {target_url}")
                    
                    flat_payload = {
                        "model": self.default_model,
                        "prompt": str(payload),
                        "stream": False,
                        "options": optimized_options # Inject caching controls globally
                    }
                    
                    response = await client.post(
                        target_url,
                        json=flat_payload,
                        timeout=float(self.timeout)
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data.get("response", "")

            except httpx.HTTPStatusError as http_err:
                logger.error(f"[LLMService HTTP Error] Status {http_err.response.status_code}: {http_err.response.text}")
                raise Exception(f"Ollama execution node rejected payload: {http_err.response.text}")
            except Exception as e:
                logger.error(f"[LLMService Exception] Critical communication breakdown: {str(e)}")
                raise e