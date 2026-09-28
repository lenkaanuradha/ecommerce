import os

from bson import ObjectId
from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient

from backend.database.User import User

MONGOURL= os.getenv("MONGOURL")
    
client = MongoClient(MONGOURL)
db = client["Users"]
users_collection = db["users_collection"]

router = APIRouter()

class createUser(BaseModel):

 @router.get("/")
 async def homepage():
    return {
        "msg": "Welcome user!",
    }

#create user end point - we are creating objects(real life entities of the class user)
 @router.post("/create_user/")
 #dependency injection- what is needed by the function is provided as a parameter, in this case the User object is injected into the function
 async def create_user(user_data: User):
    username = user_data.username
    useremail = user_data.useremail
    address = user_data.address
    new_user = users_collection.insert_one({
        "username": username,
        "useremail": useremail,
        "address": address
    })
    return {
        "msg": "user created succesfully",
        "new_user": str(new_user.inserted_id)
    }

#get a particular user
#cohesion as all user related functions are in this createUser class
 @router.get("/get_user/{id}")
 async def get_user(id: str):
    #abstraction- here don't need to know how find_one works, just use it to get the user
    user = users_collection.find_one({"_id": ObjectId(id)})
    return {
        "msg": f"retrieved user with id {id}",
        "username": user["username"],
        "useremail": user["useremail"],
        "address": user["address"]

    }

#get all users
 @router.get("/get_users/")
 async def get_users():
    users = list(users_collection.find())
    for user in users:
        user["_id"] = str(user["_id"])

    return {
        "msg": "retrieved all users",
        "users": users
    }

#Inversion of Control (IoC) - a software design principle where you hand over the control of program flow, object creation, and dependency management to an external framework or container instead of managing them inside your own code
 
 # ex-so here when we trigger http request it knows which function to call and how to create the necessary objects and manage dependencies.

 #S- Single responsibility Principle- each class should have only one responsibility, here createUser class is responsible for user related operations
 #O- Open/Closed Principle- classes should be open for extension but closed for modification - for example, we can extend the createUser class to add more user-related functionality without modifying the existing code
 #L- Liskov Substitution Principle- objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program
 #I- Interface Segregation Principle- clients should not be forced to depend on interfaces they do not use
 #"I can apply the Interface Segregation Principle by separating user-related and item-related interfaces, so a user service only depends on the user operations it needs and is not forced to depend on item operations."
 #D- Dependency Inversion Principle- high-level modules should not depend on low-level modules, both should depend on abstractions