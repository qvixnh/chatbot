from pydantic import BaseModel

class ConvesationLikeRequest(BaseModel):
    sessionId: int
    isLiked: bool