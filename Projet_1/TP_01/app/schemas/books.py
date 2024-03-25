from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    editor: str = Field(min_length=3, max_length=50)