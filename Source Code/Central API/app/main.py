from fastapi import FastAPI
from .routers import users, authentication, prices, reservations
from .db import connect_to_mongo, close_mongo_connection

#============================================================
#   Metadata/Constants
#============================================================

description = """
A centralized RESTful API for the Smart Parking System applications
"""


#============================================================
#   Application setup
#============================================================

app = FastAPI(
    title="Central API",
    description=description,
    version="0.1.0"
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo(app)
    
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection(app)

#============================================================
#   Register the routes
#============================================================

app.include_router(users.router)
app.include_router(prices.router)
app.include_router(reservations.router)
app.include_router(authentication.router)


@app.get("/")
async def root():
    return {"message": "FastAPI Central Server"}