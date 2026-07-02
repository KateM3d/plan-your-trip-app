from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.trip_request import TripRequest
from app.models.trip_option import TripOption


class TripRequestRepository:

    def create(self, db: Session, trip: TripRequest):
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return trip


    def get_all(self, db: Session):
        return db.query(TripRequest).all()

    def get_trip_by_id(self, db: Session, trip_id):
        return(
            db.query(TripRequest)
            .filter(TripRequest.id == trip_id)
            .first()
        )

    def get_trips_by_destination(self, db: Session, trip_destination: str):
        return(
            db.query(TripRequest)
            .filter(TripRequest.destination == trip_destination)
            .all()
        )

    def get_trips_by_number_of_travelers(self, db: Session, travelers: int):
        return(
            db.query(TripRequest)
            .filter(TripRequest.travelers == travelers)
            .all()
        )

    def get_trips_by_starting_location(self, db: Session, starting_location: str):
        normalized = starting_location.strip().lower()
        return (
            db.query(TripRequest)
            .filter(func.lower(TripRequest.starting_location) == normalized)
            .all()
        )
    
    def delete_request(self, db: Session, id: str):
        request = (
            db.query(TripRequest)
            .filter(TripRequest.id == id)
            .first()
        )
        if not request:
            return None
        request.is_deleted = True
        request.is_active = False
        db.query(TripOption).filter(
            TripOption.trip_request_id == id
        ).update(
            {TripOption.is_deleted: True, TripOption.is_saved: False},
            synchronize_session=False,
        )
        db.commit()
        db.refresh(request)
        return request