from pydantic import field_validator, BaseModel, Field, EmailStr
from typing import Optional
import datetime
from bson import ObjectId

#Lets change the structure of payment fields after to nested type: {payment_methods: [list of payment data types]}
# and fix the card expiry date type
class UserBase(BaseModel):
    user_name: str
    name: str
    email: str
    payment_card: str
    card_expiry_date: datetime.datetime
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    payment_card: Optional[str] = None
    card_expiry_date: Optional[datetime.datetime] = None
    password: Optional[str] = None
    
class User(UserBase):
    id: str = Field(..., alias="_id")
    
    class Config:
        populate_by_name = True
        from_attributes = True
        
    @field_validator("id", mode="before")
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
#Maybe move next 2 to separate file later on
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_name: str | None = None
    
class UserSignUp(User):
    token: Token