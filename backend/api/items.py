import os
from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from backend.database.Item import Item

MONGOURL= os.getenv("MONGOURL")
    
client = MongoClient(MONGOURL)
db = client["Items"]
items_collection = db["items_collection"]

router = APIRouter()

class createItem(BaseModel):

#create item end point
 @router.post("/store_item/")
 async def store_item(item_data: Item):
    new_item = items_collection.insert_one({
        "name": item_data.item_name,
        "price": item_data.price,
        "quantity": item_data.quantity
    })
    
    return {
        "msg": "item stored succesfully",
        "new_item": str(new_item.inserted_id),
    }

#get a particular item
 @router.get("/get_item/{id}")
 async def get_item(id: str):
    from bson import ObjectId
    item = items_collection.find_one({"_id": ObjectId(id)})
    print("here is the item",id,item)
    return {
        "msg": f"retrieved item with id {id}",
        "item_name": item["name"],
        "price": item["price"],
        "quantity": item["quantity"]
    }

#get all items
 @router.get("/get_items/")
 async def get_items():
    items = list(items_collection.find())
    new_items = []
    for item in items:
        item["_id"] = str(item["_id"])
        new_items.append(item)

    return {
        "msg": "retrieved all items",
        "items": new_items
    }

