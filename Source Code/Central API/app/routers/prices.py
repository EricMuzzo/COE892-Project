from fastapi import APIRouter, HTTPException, status
from ..models.price import Price, PriceBase  # Ensure models are properly defined
from ..crud import prices as price_crud

router = APIRouter(prefix="/pricing", tags=["Pricing"])

# Example response for OpenAPI docs
price_not_found_response = {404: {"description": "Price not found"}}

@router.get("/{time}", summary="Get price by time", description="Fetch a price based on its timestamp (MongoDB ID)", response_model=Price, responses=price_not_found_response)
async def get_price(time: str):
    """
    Fetch a price based on its timestamp (MongoDB ID).
    """
    price = await price_crud.fetch_price(time)
    if price:
        return price
    raise HTTPException(status_code=404, detail=f"Price at time {time} not found")

@router.get("/occupied-spaces/{time}", summary="Get number of occupied spaces", description="Fetch number of occupied spaces at a given time", response_model=int, responses=price_not_found_response)
async def get_occupied_spaces(time: str):
    """
    Fetch the number of occupied spaces at a given time.
    """
    # Replace this with actual logic to fetch occupied spaces
    occupied_spaces = await price_crud.fetch_occupied_spaces(time)
    if occupied_spaces is not None:
        return occupied_spaces
    raise HTTPException(status_code=404, detail=f"Occupied spaces data at time {time} not found")

@router.get("/total-spaces/", summary="Get total number of spaces", description="Fetch total number of spaces", response_model=int)
async def get_total_spaces():
    """
    Fetch the total number of spaces.
    """
    # Replace this with actual logic to fetch total spaces
    total_spaces = await price_crud.fetch_total_spaces()
    if total_spaces is not None:
        return total_spaces
    raise HTTPException(status_code=404, detail="Total spaces data not found")

@router.post("/", summary="Create a new price", description="Add a calculated price to the database", response_model=Price, status_code=status.HTTP_201_CREATED)
async def create_price(price: PriceBase):
    """
    Add a calculated price to the database.
    """
    new_price = await price_crud.create_price(price.model_dump())
    if new_price:
        return new_price
    raise HTTPException(status_code=400, detail="Price creation failed")
