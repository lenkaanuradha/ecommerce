from pydantic import BaseModel, EmailStr


# here encapsulation is used - as it groups related attributes together and pydantic validation
class User(BaseModel):
    username: str
    useremail: EmailStr
    address: str