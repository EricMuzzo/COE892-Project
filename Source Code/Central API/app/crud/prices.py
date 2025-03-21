from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument

from ..models.price import Price  # Ensure the Price model is imported
from ..utils.db import prices_collection   # Assuming you have a prices collection in your DB

async def fetch_all_prices(filters: dict = {}) -> list:
    """
    Returns a list of price objects from the prices collection in the database.
    Filters can be applied to query specific prices.

    Args:
        filters (dict): Optional filters to query prices (e.g., {"time": "2025-03-08T16:30:00"}).

    Returns:
        list: A list of price dictionaries.
    """
    prices = await prices_collection.find(filters).to_list(1000)
    return prices


async def fetch_price(id: str) -> dict | None:
    """
    Returns a single price object from the prices collection by its MongoDB ObjectId.

    Args:
        id (str): The MongoDB ObjectId of the price.

    Returns:
        dict | None: The price dictionary if found, otherwise None.
    """
    price = await prices_collection.find_one({"_id": ObjectId(id)})
    return price


async def create_price(price_data: dict) -> dict:
    """
    Inserts a new price record into the prices collection.

    Args:
        price_data (dict): The price data to insert.

    Raises:
        HTTPException: If a duplicate key error occurs (e.g., duplicate timestamp).

    Returns:
        dict: The created price object.
    """
    try:
        new_price = await prices_collection.insert_one(price_data)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="A price with the provided timestamp already exists")

    created_price = await prices_collection.find_one({"_id": new_price.inserted_id})
    return created_price


async def update_price(id: str, data: dict) -> dict | JSONResponse:
    """
    Updates a price document in the prices collection by its MongoDB ObjectId.

    Args:
        id (str): The MongoDB ObjectId of the price to update.
        data (dict): The fields to update.

    Returns:
        dict | JSONResponse: The updated price dictionary or a JSONResponse if a duplicate key error occurs.
    """
    if len(data) >= 1:
        try:
            update_result = await prices_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": data},
                return_document=ReturnDocument.AFTER
            )
        except DuplicateKeyError:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Duplicate key error",
                    "message": "A price with the provided timestamp already exists"
                }
            )
        return update_result

    # If no update data is provided, return the existing price
    existing_price = await prices_collection.find_one({"_id": ObjectId(id)})
    return existing_price


async def remove_price(id: str) -> bool:
    """
    Deletes a price document from the prices collection by its MongoDB ObjectId.

    Args:
        id (str): The MongoDB ObjectId of the price to delete.

    Returns:
        bool: True if the deletion was successful, otherwise False.
    """
    result = await prices_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return True
    return False
