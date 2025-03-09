from pydantic import field_validator, BaseModel, Field, EmailStr

class ParkingSpot(BaseModel):
    floor_level: int
    spot_number: int
    status: str