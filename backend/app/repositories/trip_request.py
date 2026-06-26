from sqlalchemy.orm import Session
from backend.app.models.trip_request import TripRequest


class TripRequestRepository:

    def create(self, db: Session, trip: TripRequest):
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return trip


    def get_all(self, db: Session):
        return db.query(TripRequest).all()

    def get_by_ad(self, db: Session, trip_id):
        return(
            db.query(TripRequest)
            .filter(TripRequest.id == trip_id)
            .first()
        )
        