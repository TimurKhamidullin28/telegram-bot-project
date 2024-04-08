from database.common.models import db, BaseModel


def create_models():
    db.create_tables(BaseModel.__subclasses__())
