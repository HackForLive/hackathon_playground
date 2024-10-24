from pydantic import BaseModel, Field

class UserQuery(BaseModel):
    prompt: str
    temperature: float = Field(None, ge=0.0, le=1.0)
    # optional params
