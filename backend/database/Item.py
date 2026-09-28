from pydantic import BaseModel, EmailStr
from typing import Optional

class Item(BaseModel):
    item_name: str
    price: float
    category: str
    quantity: int