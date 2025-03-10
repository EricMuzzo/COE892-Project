from pydantic import field_validator, BaseModel, Field
from bson import ObjectId

class ParkingSpotBase(BaseModel):
    floor_level: int
    spot_number: int
    occupied: bool
    
class ParkingSpot(ParkingSpotBase):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True
        from_attributes = True
        
    @field_validator("id", mode="before")
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v