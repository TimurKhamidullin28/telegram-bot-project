import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_PATH = os.path.join('/sqlite', 'kp_database.db')

BOT_TOKEN = os.getenv("BOT_TOKEN")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")

BASE_URL = 'https://api.kinopoisk.dev/v1.4/movie'

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку по командам бота"),
    ("movie", "Найти фильм по названию"),
    ("history", "История поиска"),
    ("genre_and_rt", "Поиск фильмов по жанру и рейтингу")
)
