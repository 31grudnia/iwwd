from sqlalchemy.orm import Session

from database.models.StatusModel import Status as StatusModel


def get_status_by_id(db: Session, index: int):
    return db.query(StatusModel).filter(StatusModel.id == index).first()