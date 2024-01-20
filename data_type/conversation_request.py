from pydantic import BaseModel

class ConvesationRequest(BaseModel):
    sessionId: int
    text: str