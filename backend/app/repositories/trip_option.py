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