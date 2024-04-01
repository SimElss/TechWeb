from pydantic import BaseModel, field_validator

class UserSchema(BaseModel):
    id: str
    username: str
    name: str
    surname: str
    password: str
    email: str
    group: str

    @field_validator('password')
    @classmethod
    def validate_password_capital(cls, value):
        has_capital = any([char.isupper() for char in value]) and any([char.islower() for char in value]) and any([char.isdigit() for char in value]) and any([char in "!@#$%^&*()-+" for char in value])
        if not has_capital:
            raise ValueError("""Password must contain at least one capital letter""")
        return value
