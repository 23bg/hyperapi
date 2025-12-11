# app/main.py
from racerapi.core.app_factory import racerAPI
from racerapi.core.settings import AppSettings
from racerapi.core.application import Application
from app.core.logging import logger

settings = AppSettings(
   title="My AI Backend",
    version="1.2.0",
    cors_origins=["*"],
    description="Enterprise AI Backend built on RacerAPI", 
    middlewares=[
        Application.add_middleware(logger())
        
    ]
)


app = racerAPI(settings)
