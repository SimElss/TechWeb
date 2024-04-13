from pydantic import BaseModel, field_validator
from pydantic.fields import Field

#Schema of users -> we don't use password_confirm in it it's verified in services
class UserSchema(BaseModel):
    id: str
    username: str
    name: str
    surname: str
    password: str
    email: str
    group: str # admin or client
    whitelist: bool # Blocked or not

    #Custome rule for password
    @field_validator('password')
    @classmethod
    def validate_password_capital(cls, value):
        has_capital = any([char.isupper() for char in value]) and any([char.islower() for char in value]) and any([char.isdigit() for char in value]) and any([char in "!@#$%^&*()-+" for char in value]) and len(value) >= 8
        if not has_capital:
            raise ValueError("""Le mot de passe doit contenir au moins une majuscule, un nombre, un caractère spéciale et faire plus de 8 caractères""")
        return value
    
class Token(BaseModel):
    acces_token: str
    token_type: str
    