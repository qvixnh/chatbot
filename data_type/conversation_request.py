from pydantic import BaseModel

class ConvesationRequest(BaseModel):
    sessionId: int
    text: str
class ConvesationRequestInput(BaseModel):
    sessionId: int
    text: str
class ConvesationLikeRequest(BaseModel):
    sessionId: str
    isLiked: bool
class dayLimitRequest(BaseModel):
    sessionId: str
    dayLimit: int