from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str
    name: str = Field(min_length=3, max_length=50)
    author: str
    editor: str