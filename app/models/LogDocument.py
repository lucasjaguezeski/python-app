from datetime import datetime, timezone
from typing import Any, Annotated
from beanie import Document, Indexed
from pydantic import Field
from enum import Enum


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"


class LogDocument(Document):
    timestamp: Annotated[
        datetime, Indexed, Field(default_factory=lambda: datetime.now(timezone.utc))
    ]
    level: Annotated[LogLevel, Indexed] = LogLevel.INFO
    message: Annotated[str, Field(description="The log message content")]
    endpoint: Annotated[str | None, Indexed] = None
    method: Annotated[
        str | None, Field(description="HTTP method (e.g., GET, POST)")
    ] = None
    metadata: Annotated[dict[str, Any] | None, Field(default=None)] = None

    class Settings:
        name = "app_logs"
