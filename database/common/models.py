from config_data.config import DB_PATH
from peewee import AutoField, CharField, DateField, ForeignKeyField, IntegerField, Model, SqliteDatabase

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


class History(BaseModel):
    history_id = AutoField()
    user = ForeignKeyField(User, backref="history")
    title = CharField()
    created_at = DateField()

    def __str__(self):
        return '{date} - {film_title}'.format(
            date=self.created_at,
            film_title=self.title
        )


class Movie:
    def __init__(self, id_movie, name, year, country, genre, rating_kp, rating_imdb, description, poster_url):
        self.id_movie = id_movie,
        self.name = name,
        self.year = year,
        self.country = country,
        self.genre = genre,
        self.rating_kp = rating_kp,
        self.rating_imdb = rating_imdb,
        self.description = description,
        self.poster_url = poster_url

    def __str__(self):
        text = f'Информация о фильме: \n\n'\
               f'Название: {str(*self.name)}\nГод: {int(*self.year)}\nСтрана: {str(*self.country)}\n'\
               f'Жанр: {str(*self.genre)}\nРейтинг КП: {float(*self.rating_kp)}\n'\
               f'Рейтинг IMDb: {float(*self.rating_imdb)}\n'\
               f'Краткое описание: {str(*self.description)}\nПостер: {self.poster_url}\n'

        return text
