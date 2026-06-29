from datetime import datetime
import uuid
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

    