from pydantic import BaseModel, Field

class UserQuery(BaseModel):
    prompt: str
    temperature: float = Field(0.0, ge=0.0, le=1.0)
    # optional params
