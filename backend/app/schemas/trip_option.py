from datetime import datetime
import uuid
from pydantic import BaseModel


class TripOptionCreate(BaseModel):
    title: str
    short_description: str
    estimated_budget: int
    trip_request_id: uuid.UUID

class TripOptionResponse(BaseModel):
    id: uuid.UUID
    trip_request_id: uuid.UUID
    title: str
    short_description: str
    estimated_budget: int
    created_at: datetime
    is_saved: bool
    is_deleted: bool

    class Config:
        from_attributes = True