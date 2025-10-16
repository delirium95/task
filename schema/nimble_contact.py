from pydantic import BaseModel, Field, ConfigDict


class NimbleContact(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    description: str = Field(...)