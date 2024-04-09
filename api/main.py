import json
from typing import Any, List
import requests
from requests import ReadTimeout, Response

from config_data.config import BASE_URL, KINOPOISK_API_KEY
from database.common.models import Movie
from utils.create_movie_list import create_movie_list


def api_request(endpoint: str, headers, params) -> requests.Response:
    return requests.get(
        f'{BASE_URL}/{endpoint}',
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
            return response
    except ReadTimeout:
        print('Не удалось получить информацию о фильме')


def get_movie(id_number: int) -> List[Movie]:
    result = list()
    response = api_request(f'{id_number}', headers={
        'X-API-KEY': KINOPOISK_API_KEY}, params={})
    result.append(json.loads(response.text))
    new_result = create_movie_list(result)
    return new_result
