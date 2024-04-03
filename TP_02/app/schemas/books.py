from pydantic import BaseModel, Field
from typing import Optional



class Book(BaseModel):
    id: str
    name: str
    Author: str
    Editor: Optional[str] = None