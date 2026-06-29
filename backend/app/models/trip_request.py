import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func

from app.db.session import Base

class TripRequest(Base):
    __tablename__ = "trip_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    destination = Column(String, nullable=False)
    starting_location = Column(String, nullable=False)
    budget = Column(Integer, nullable=False)
    currency = Column(String, default="EUR")
    travelers = Column(Integer, nullable=False)
    departure_datetime = Column(DateTime(timezone=True), nullable=False)
    return_datetime = Column(DateTime(timezone=True), nullable=False)
    user_preferences = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)