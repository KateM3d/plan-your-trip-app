from sqlalchemy.orm import Session

from app.models.trip_option import TripOption


class TripOptionRepository:

    def create(self, db: Session, option: TripOption):
        db.add(option)
        db.commit()
        db.refresh(option)
        return option