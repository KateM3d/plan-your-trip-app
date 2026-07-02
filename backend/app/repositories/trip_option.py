from sqlalchemy.orm import Session

from app.models.trip_option import TripOption


class TripOptionRepository:

    def create(self, db: Session, option: TripOption):
        db.add(option)
        db.commit()
        db.refresh(option)
        return option

    def get_all_options(self, db: Session):
        return  db.query(TripOption).all()

    def get_option_by_id(self, db: Session, id: str):
        return(
            db.query(TripOption)
            .filter(TripOption.id == id)
            .first()
        )

    def get_all_options_by_trip_request_id(self, db: Session, trip_request_id: str):
        return(
            db.query(TripOption)
            .filter(TripOption.trip_request_id == trip_request_id)
            .all()
        )

    def delete_option(self, db: Session, id: str):
        option = (
            db.query(TripOption)
            .filter(TripOption.id == id)
            .first()
        )
        if not option:
            return None
        option.is_deleted = True
        db.commit()
        db.refresh(option)
        return option