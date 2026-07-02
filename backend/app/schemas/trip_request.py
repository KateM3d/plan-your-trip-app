from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid


class TripRequestCreate(BaseModel):
    destination: str
    starting_location: str
    budget: int
    currency: str = "EUR"
    travelers: int
    departure_datetime: datetime
    return_datetime: datetime
    user_preferences: Optional[str] = None


class TripRequestResponse(BaseModel):
    id: uuid.UUID
    destination: str
    starting_location: str
    budget: int
    currency: str
    travelers: int
    departure_datetime: datetime
    return_datetime: datetime
    user_preferences: Optional[str] = None
    created_at: datetime
    is_active: bool
    is_completed: bool
    is_deleted: bool

    class Config:
        from_attributes = True