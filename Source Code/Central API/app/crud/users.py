from fastapi import HTTPException
from ..schemas.user import user_serial
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..utils.auth import get_password_hash

async def fetch_all_users(database: AsyncIOMotorDatabase, filters: dict = {}) -> list:
    """Returns a list of users from the users collection in database"""
    users = []
    cursor = database["users"].find(filters)
    async for document in cursor:
        users.append(user_serial(document))
    return users

async def fetch_user(database: AsyncIOMotorDatabase, id: str) -> dict:
    """Return a dict of a single user with user_id"""
    document = await database["users"].find_one({"_id": ObjectId(id)})
    if document:
        return user_serial(document)
    return None

async def create_user(database: AsyncIOMotorDatabase, user_data: dict) -> dict:
    """Returns a dict of the created user"""
    result = await database["users"].insert_one(user_data)
    new_user = await database["users"].find_one({"_id": result.inserted_id})
    return user_serial(new_user)

async def update_user(database: AsyncIOMotorDatabase, id: str, data: dict):
    
    if "password" in data:
        data["password"] = get_password_hash(data["password"])
    
    data = {k: v for k, v in data.items() if v is not None}
    if data:
        result = await database["users"].update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count:
            updated_user = await database["users"].find_one({"_id": ObjectId(id)})
            if updated_user:
                return user_serial(updated_user)
    existing_user = await database["users"].find_one({"_id": ObjectId(id)})
    if existing_user:
        return user_serial(existing_user)
    return None


async def remove_user(database: AsyncIOMotorDatabase, id: str):
    result = await database["users"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return True
    return False