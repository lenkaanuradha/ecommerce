from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.database.Item import Item

#Composistion - an order is composed of multiple items, hence it has a list of Item objects
class Order(BaseModel):
    user_id: int
    total_price: float
    total_items: list[Item]