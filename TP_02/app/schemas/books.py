from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str
    name: str
    Author: str
    Editor: str