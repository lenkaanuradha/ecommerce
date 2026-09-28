import os
from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from backend.database.Item import Item

MONGOURL= os.getenv("MONGOURL")
    
client = MongoClient(MONGOURL)
db = client["Orders"]
orders_collection = db["orders_collection"]

router = APIRouter()

class createOrder(BaseModel):

#create order end point
#coupling is used here as it depends on the Item class to create an order
 @router.post("/create_order/{userid}")
 async def create_order(userid: str,items: list[Item],discount: float):
    userid = userid
    total_price = 0
    discount = discount
    total_items = []
    for item in items:
        total_price += item.price * item.quantity
        total_items.append({
            "item_name": item.item_name,
            "price": item.price,
            "quantity": item.quantity
        })
    new_order = orders_collection.insert_one({
        "user_id": userid,
        "total_price": total_price - discount,
        "total_items": total_items
    })
    new_order = orders_collection.find_one({"_id": new_order.inserted_id})  
    return {
        "msg": "order created succesfully",
        "new_order": {
            "_id": str(new_order["_id"]),
            "user_id": new_order["user_id"],
            "total_price": new_order["total_price"],
            "total_items": new_order["total_items"]
        },
    }

#get a particular order
 @router.get("/get_order/{id}")
 async def get_order(id: str):
    from bson import ObjectId
    order = orders_collection.find_one({"_id": ObjectId(id)})
    return {
        "msg": f"retrieved order with id {id}",
        "order": order
    }

#get all orders
 @router.get("/get_orders/")
 async def get_orders():
    orders = list(orders_collection.find())
    for order in orders:
        order["_id"] = str(order["_id"])

    return {
        "msg": "retrieved all orders",
        "orders": orders
    }

#L- Liskov Substitution Principle- objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program
 #example- 
#  class calcTotalPrice: --> parent
#     def calculate(self, items: list[Item], discount: float) -> float:
#         total_price = 0
#         for item in items:
#             total_price += item.price * item.quantity
#         return total_price
#@router.post("/create_order/{userid}")
#  class caltotalwithdiscount(calcTotalPrice): --> child
#     def calculate(self, items: list[Item], discount: float) -> float:
#         total_price = super().calculate(items, 0)
#         return total_price - discount

#The Interface Segregation Principle (ISP) suggests that a class should not be forced to implement methods it doesn’t need

# DIP says:

# High-level code should not depend directly on a concrete low-level implementation. Both should depend on an abstraction.