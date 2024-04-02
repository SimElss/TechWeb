from pydantic import BaseModel, field_validator
from pydantic.fields import Field

class UserSchema(BaseModel):
    id: str
    username: str
    name: str
    surname: str
    password: str = Field(min_length=8)
    email: str
    group: str
    whitelist: bool

    @field_validator('password')
    @classmethod
    def validate_password_capital(cls, value):
        has_capital = any([char.isupper() for char in value]) and any([char.islower() for char in value]) and any([char.isdigit() for char in value]) and any([char in "!@#$%^&*()-+" for char in value]) and len(value) >= 8
        if not has_capital:
            raise ValueError("""Password must contain at least one capital letter, a digit and a special character and must be at least len of 8 characters.""")
        return value
