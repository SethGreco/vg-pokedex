from typing import Optional, List
from pydantic import BaseModel

class Pokemon(BaseModel):
    number: int
    name: str
    species: str
    height: str
    weight: Optional[float] 
    description: Optional[str] 
    area: Optional[str] 


class Error(BaseModel):
    loc: Optional[List[str]] = None
    msg: str
    type: str

class ErrorResponse(BaseModel):
    detail: List[Error]

class Message(BaseModel):
    detail: str
