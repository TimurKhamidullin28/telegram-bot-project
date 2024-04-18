# Telegram-бот для работы с API Кинопоиска
Проект, разработанный на языке Python, для взаимодействия с [API Кинопоиска] (https://kinopoisk.dev/)

## Навигация

* [Начало работы](#начало-работы)
  * [Установка зависимостей](#установка-зависимостей)
  * [Получение ключа от API Кинопоиска](#получение-ключа-от-api-кинопоиска)
* [Получение информации о фильме по ID Кинопоиска](#получение-информации-о-фильме-по-id-кинопоиска)
  * [Описание функции get_movie](#описание-функции-get_movie)
  * [Применение функции get_movie в Telegram-боте](#применение-функции-get_movie-в-telegram-боте)
* [Поиск фильма через API Кинопоиска по названию](#поиск-фильма-через-api-кинопоиска-по-названию)
  * [Описание функции find_movie](#описание-функции-find_movie)
  * [Применение функции find_movie в Telegram-боте](#применение-функции-find_movie-в-telegram-боте)
* [Поиск фильма через API Кинопоиска по жанру и рейтингу](#поиск-фильма-через-api-кинопоиска-по-жанру-и-рейтингу)
  * [Описание функции find_by_genre_and_rt](#описание-функции-find_by_genre_and_rt)
  * [Применение функции find_by_genre_and_rt в Telegram-боте](#применение-функции-find_by_genre_and_rt-в-telegram-боте)

## Начало работы
Для работы Вам нужно клонировать репозиторий в Ваш проект.  Воспользуйтесь [ссылкой на репотизотрий] (https://gitlab.skillbox.ru/timur_khamidullin/diploma_python_basic)

### Установка зависимостей
```
pip install -r requirements.txt
```

### Получение ключа от API Кинопоиска
Для работы с API Кинопоиска Вам необходимо получить токен в боте [@kinopoiskdev_bot](https://t.me/kinopoiskdev_bot).  После получения токена, Вам необходимо авторизоваться в [Документации] (https://api.kinopoisk.dev/documentation), для этого нажмите на кнопку **Authorize** и введите токен в поле **Value**.

## Получение информации о фильме по ID Кинопоиска
```python
from api.main import get_movie

film = get_movie(500)

print(*film[0].name, *film[0].year)
print(*film[0].genre)
print(*film[0].country)
```

```
>>> Собачий полдень 1975
>>> триллер, драма, криминал, биография
>>> США
```

### Описание функции `get_movie`
Функция get_movie получает на вход целое число - ID фильма на Кинопоиске.  С помощью функции `api_request` на сервер отправляется GET-запрос с указанием url, headers (в том числе и Ваш ключ от API Кинопоиска) и params. Полученный ответ преобразуется в формат json и добавляется в пустой список.  Далее элементы этого списка обрабатываются функцией `create_movie_list`, определенной в пакете utils, которая возвращает список объектов класса Movie (определенный в файле `database.common.models.py`).  В результате функция `get_movie` возвращает список из одного объекта класса Movie.

Параметры объекта класса Movie, возвращаемый функцией `get_movie`:
* ID фильма на Кинопоиске - `self.id_movie`
* Название фильма на русском языке - `self.name`
* Год премьеры фильма - `self.year`
* Список с странами производства - `self.country`
* Список с жанрами - ` self.genre`
* Рейтинг на Кинопоиске - `self.rating_kp`
* Рейтинг на IMDb - `self.rating_imdb`
* Описание фильма - `self.description` (В случае отсутствия возвращается 'не найдено')
* Ссылка на изображение постера - `self.poster_url` (В случае отсутствия возвращается 'не найден')

### Применение функции `get_movie` в Telegram-боте
Функция get_movie вызывается при нажатии кнопок в обработчике `callback_query_handler`:

```python
@bot.callback_query_handler(func=lambda message: True)
def callback_query(message):
    bot.send_message(message.from_user.id, *get_movie(message.data))
```

## Поиск фильма через API Кинопоиска по названию
```python
from api.main import find_movie
from utils.create_movie_list import create_movie_list

search = find_movie('королева')
movies = create_movie_list(search['docs'])

for movie in movies:
    print(*movie.name, *movie.year)
    print(*movie.genre)
    print(*movie.country)
```

```
>>> Королева 2005
>>> драма, биография
>>> Великобритания, США, Франция, Италия
>>> ...
```

### Описание функции `find_movie`
У функции find_movie имеется обязательный аргумент title, по которому будет производиться поиск, а также именнованные аргументы page (страница выборки, по умолчанию равен 1) и limit (количество элементов на странице, по умолчанию 10).  Посредством функции `api_request` на сервер отправляется GET-запрос с указанием url (endpoint='search'), headers и params ('page': page, 'limit': limit, 'query': title).  При успешном выполнении запроса, код 200, функция `find_movie` возвращает ответ от сервера, преобразованный в формат json. Иначе возвращает информацию об ошибке.

### Применение функции `find_movie` в Telegram-боте
Функция find_movie используется в обработчике, расположенным в файле `handlers.custom_handlers.find_movie.py`, при вводе пользователем названия фильма (команда /movie).

```python
@bot.message_handler(content_types=['text'], state=UserState.film_title)
def process_film_title(message: Message) -> None:
    ...
    response = api.main.find_movie(title=message.text)
    ...
```

## Поиск фильма через API Кинопоиска по жанру и рейтингу
```python
from api.main import find_by_genre_and_rt
from utils.create_movie_list import create_movie_list

search = find_by_genre_and_rt(genre_name='комедия', rating=8.3, quantity=5)
movies = create_movie_list(search['docs'])

for movie in movies:
    print(*movie.name, *movie.year)
    print(*movie.genre)
    print(*movie.country)
```

```
>>> 1+1 2011
>>> драма, комедия, биография
>>> Франция
>>> ...
```

### Описание функции `find_by_genre_and_rt`
У функции есть обязательные аргументы: genre_name, rating и quantity (жанр, рейтинг и количество фильмов, соответственно), по которым будет производиться поиск. По аналогии с функцией `find_movie` на сервер отправляется GET-запрос с указанием следующих параметров(params):  'page': 1, 'limit': quantity, 'rating.imdb': `f'{rating}-10'`, 'genres.name': `genre_name.lower()`, 'type': 'movie'.  Функция `find_by_genre_and_rt` возвращает ответ от сервера, преобразованный в формат json.

### Применение функции `find_by_genre_and_rt` в Telegram-боте
Функция используется в обработчике, расположенным в файле `handlers.custom_handlers.searchByGenreAndRt.py`, при вводе пользователем количества фильмов (команда /genre_and_rt).

```python
@bot.message_handler(state=UserState.quantity_films)
def process_quantity_films(message: Message) -> None:
    ...
    response = find_by_genre_and_rt(genre_name=data["genre"],
                                    rating=data["rating"],
                                    quantity=data["total_films"])
    ...
```
