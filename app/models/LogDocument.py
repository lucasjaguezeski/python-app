from datetime import datetime, timezone
from typing import Optional, Any, Dict
from beanie import Document
from pydantic import Field
from enum import Enum


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"


class LogDocument(Document):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    level: LogLevel = LogLevel.INFO
    message: str
    endpoint: Optional[str] = None
    method: Optional[str] = None
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    class Settings:
        name = "app_logs"
        indexes = ["timestamp", "level", "endpoint"]
