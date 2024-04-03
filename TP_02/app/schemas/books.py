from pydantic import BaseModel, Field
from typing import Optional


#Schema of books
class Book(BaseModel):
    id: str
    name: str
    Author: str
    Editor: Optional[str] = None #Editor is optional <=> str | None