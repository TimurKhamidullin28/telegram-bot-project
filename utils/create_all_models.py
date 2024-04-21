from database.common.models import db, BaseModel


def create_models():
    """
    Функция, которая создает в базе данных все модели, наследуемые от общего класса BaseModel
    """
    with db:
        db.create_tables(BaseModel.__subclasses__())
