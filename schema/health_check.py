from pydantic import BaseModel, Field


class HealthCheckResponseDB(BaseModel):
    response: bool = Field(..., description="Database connection status")
