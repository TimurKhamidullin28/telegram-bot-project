import json
from typing import Any, List
import requests
from requests import ReadTimeout, Response

from config_data.config import BASE_URL, KINOPOISK_API_KEY
from database.common.models import Movie
from utils.create_movie_list import create_movie_list


def api_request(endpoint: str, headers, params) -> requests.Response:
    return requests.get(
        f'{BASE_URL}/{endpoint}' if endpoint else f'{BASE_URL}',
        headers=headers,
        params=params,
        timeout=15
    )


def find_movie(title: Any, page: int = 1, limit: int = 10) -> Response:
    try:
        response = api_request('search', params={
            'page': page,
            'limit': limit,
            'query': title.lower() if isinstance(title, str) else title
        }, headers={'X-API-KEY': KINOPOISK_API_KEY})
        if response.status_code == requests.codes.ok:
            result = json.loads(response.text)
            return result
    except ReadTimeout:
        print('Не удалось получить информацию о фильме')


def get_movie(id_number: int) -> List[Movie]:
    result = list()
    response = api_request(f'{id_number}', headers={
        'X-API-KEY': KINOPOISK_API_KEY}, params={})
    if response.status_code == requests.codes.ok:
        result.append(json.loads(response.text))
        new_result = create_movie_list(result)
        return new_result


def find_by_genre_and_rt(genre_name: str, rating: int or float, quantity: int) -> Response:
    response = api_request('', params={
        'page': 1,
        'limit': quantity,
        'rating.imdb': f'{rating}-10',
        'genres.name': genre_name.lower(),
        'type': 'movie'
    }, headers={'X-API-KEY': KINOPOISK_API_KEY})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        return data
