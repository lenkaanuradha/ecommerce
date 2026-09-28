from fastapi import FastAPI

from backend.api import items, orders, users

app = FastAPI()

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(items.router)