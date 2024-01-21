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


class PokemonShort(BaseModel):
    number: int
    name: str


class Title(BaseModel):
    id: int
    pokemonGame: str


class Error(BaseModel):
    loc: Optional[List[str]] = None
    msg: str
    type: str


class ErrorResponse(BaseModel):
    detail: List[Error]


class Message(BaseModel):
    detail: str


# For Security
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
