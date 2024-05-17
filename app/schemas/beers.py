from pydantic import BaseModel
from typing import Optional


#Schema of Beers
class Beer(BaseModel):
    id: str
    name: str
    Author: str
    Editor: Optional[str] = None #Editor is optional <=> str | None
    price: float
    bought: bool
    new_owner_id: Optional[str] = None