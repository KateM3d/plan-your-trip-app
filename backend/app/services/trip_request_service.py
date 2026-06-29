import datetime
from typing import List
import uuid
from sqlalchemy.orm import Session
from app.models.trip_request import TripRequest
from app.schemas.trip_request import TripRequestCreate
from app.repositories.trip_request import TripRequestRepository


class TripRequestService:
    def __init__(self, repo: TripRequestRepository | None = None):
        self.repo = repo or TripRequestRepository()

    def create_trip(self, data: TripRequestCreate) -> TripRequest:
        return TripRequest(
            id = uuid.uuid4(),
            destination=data.destination,
            starting_location=data.starting_location,
            budget=data.budget,
            currency=data.currency,
            travelers=data.travelers,
            departure_datetime=data.departure_datetime,
            return_datetime=data.return_datetime,
            user_preferences=data.user_preferences,
        )

    def get_all_trips(self, db: Session) -> List[TripRequest]:
        return self.repo.get_all(db)

    def get_trip_by_id(self, db: Session, trip_id: str) -> TripRequest:
        return self.repo.get_trip_by_id(db, trip_id)

    def get_trips_by_destination(self, db: Session, trip_destination: str) -> List[TripRequest]:
        return self.repo.get_trips_by_destination(db, trip_destination)

    def get_trips_by_number_of_travelers(self, db: Session, travelers: int) -> List[TripRequest]:
        return self.repo.get_trips_by_number_of_travelers(db, travelers)
    
    def get_trips_by_starting_location(self, db: Session, starting_location: str) -> List[TripRequest]:
        return self.repo.get_trips_by_starting_location(db, starting_location)