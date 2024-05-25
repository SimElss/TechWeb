from pydantic import BaseModel
from typing import Optional


#Schema of Beers
class Beer(BaseModel):
    id: str
    name: str
    brewery: str
    price: float
    stock: int
    description: str
    image: str

    @staticmethod
    def model_validate(data):
        return Beer(**data)

