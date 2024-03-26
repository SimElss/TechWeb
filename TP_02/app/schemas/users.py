from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    username: str
    username: str
    password: str
    email: str
    group: str
