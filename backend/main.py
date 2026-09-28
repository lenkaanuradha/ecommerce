from fastapi import FastAPI
from backend.api import users, orders, items

app = FastAPI()

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(items.router)