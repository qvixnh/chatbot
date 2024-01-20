from pydantic import BaseModel
from typing import Optional

class ProductRequest(BaseModel):
    name: str
    priceForm: Optional[int] = None
    priceTo: Optional[int] = None