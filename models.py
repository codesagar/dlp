from typing import List
from pydantic import BaseModel

class PANPIIRequest(BaseModel):
    text: str
    entities: List[str]

class PANPIIResponse(BaseModel):
    text: str
    entities: List[str]
    mapping: dict