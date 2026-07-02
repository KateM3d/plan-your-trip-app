from datetime import datetime
from typing import List
import uuid

from sqlalchemy.orm import Session
from app.models.trip_option import TripOption
from app.repositories.trip_option import TripOptionRepository
from app.schemas.trip_option import TripOptionCreate


class TripOptionService:
    def __init__(self, repo: TripOptionRepository | None = None):
        self.repo = repo or TripOptionRepository()

    def create_option(self, data: TripOptionCreate) -> TripOption:
        return TripOption(
            id = uuid.uuid4(),
            trip_request_id=data.trip_request_id,
            title=data.title,
            short_description=data.short_description,
            estimated_budget=data.estimated_budget,
            created_at=datetime.now(),
            is_saved=False,
            is_deleted=False,
        )

    def get_all_options(self, db: Session) -> TripOption:
        return self.repo.get_all_options(db)

    def get_option_by_id(self, db: Session, id: str) -> TripOption:
        return self.repo.get_option_by_id(db, id)

    def get_all_options_by_trip_request_id(self, db: Session, trip_request_id: str) -> List[TripOption]:
        return self.repo.get_all_options_by_trip_request_id(db,trip_request_id)

    def delete_option( self, db: Session, id: str) -> TripOption:
        return self.repo.delete_option(db, id)