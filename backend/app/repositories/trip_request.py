from sqlalchemy.orm import Session
from app.models.trip_request import TripRequest


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