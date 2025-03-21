from pydantic import BaseModel, Field, field_validator
from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated, List
from bson import ObjectId
from datetime import datetime, time, timedelta

# Reuse the PyObjectId type for MongoDB compatibility
PyObjectId = Annotated[str, BeforeValidator(str)]

class PriceBase(BaseModel):
    """Base model for pricing parameters (used for creation/updates)."""
    base_price_morning: float = Field(
        ...,
        ge=0,  # Ensures value is >= 0
        description="Base price for morning hours (e.g., 6 AM - 12 PM)",
        example=5.99
    )
    base_price_afternoon: float = Field(
        ...,
        ge=0,
        description="Base price for afternoon hours (e.g., 12 PM - 6 PM)",
        example=7.99
    )
    base_price_evening: float = Field(
        ...,
        ge=0,
        description="Base price for evening hours (e.g., 6 PM - 12 AM)",
        example=9.99
    )

class Price(PriceBase):
    """Database representation of pricing parameters."""
    id: Optional[PyObjectId] = Field(
        alias="_id",  # MongoDB uses "_id" as the primary key
        default=None,
        description="Unique identifier for the price configuration"
    )

    class Config:
        populate_by_name = True  # Allows using "id" instead of "_id" when creating instances
        json_encoders = {ObjectId: str}  # Converts ObjectId to string in JSON responses

    def calculate_price(self, reservation_start: datetime, reservation_end: datetime, total_occupied: int, total_spots: int)  -> float:
        """
        Calculate the total price for a reservation based on the time of day and duration.

        Args:
            reservation_start (datetime): Start time of the reservation.
            reservation_end (datetime): End time of the reservation.

        Returns:
            float: Total price for the reservation.
        """
        total_price = 0.0

        # Define time ranges for pricing
        morning_start = time(6, 0)  # 6 AM
        afternoon_start = time(12, 0)  # 12 PM
        evening_start = time(18, 0)  # 6 PM

        current_time = reservation_start

        while current_time < reservation_end:
            if morning_start <= current_time.time() < afternoon_start:
                price_per_hour = self.base_price_morning
            elif afternoon_start <= current_time.time() < evening_start:
                price_per_hour = self.base_price_afternoon
            else:
                price_per_hour = self.base_price_evening 

        total_price = (1+ (total_occupied/total_spots)) * price_per_hour

        return total_price

class PriceCollection(BaseModel):
    """Wrapper for a list of price configurations (useful for bulk operations)."""
    prices: List[Price]
