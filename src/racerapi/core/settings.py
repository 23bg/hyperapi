from pydantic import BaseModel
from typing import Optional, Any, List, Dict, Callable


class AppSettings(BaseModel):
    title: str = "RacerAPI"
    description: Optional[str] = None
    version: str = "0.1.0"

    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"
    openapi_url: Optional[str] = "/openapi.json"

    # Middleware configuration
    middlewares: List[Callable] = []

    # Exception handlers
    exception_handlers: Dict[Any, Callable] = {}

    # CORS config (optional)
    cors_origins: List[str] = []
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Additional routers (outside module system)
    extra_routers: List[Any] = []
