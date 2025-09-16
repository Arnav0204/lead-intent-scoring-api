from pydantic import BaseModel,Field,ValidationError
from typing import List

class OfferDTO(BaseModel):
    name        : str       = Field(...,min_length=1)
    value_props : List[str] = Field(...,min_items=1)
    ideal_use_cases: List[str] = Field(..., min_items=1)