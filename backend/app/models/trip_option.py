import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class TripOption(Base):
    __tablename__ = "trip_options"

    id - Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_request_id = Column(UUID(as_uuid=True), ForeignKey("trip_requests.id"), nullable=False)
    title = Column(String, nullable=False)
    short_description = Column(String, nullable=False)
    estimated_budget = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_saved = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)