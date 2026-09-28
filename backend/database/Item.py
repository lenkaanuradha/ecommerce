from pydantic import BaseModel


class Item(BaseModel):
    item_name: str
    price: float
    category: str
    quantity: int