from pydantic import BaseModel
from typing import Optional

class ManagerRequest(BaseModel):
    name: str