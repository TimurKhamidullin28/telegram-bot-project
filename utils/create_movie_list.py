from typing import Dict, List
from database.common.models import Movie


def create_movie_list(lst: List[Dict]) -> List[Movie]:
    """
    Функция, преобразующая ответы в формате json, полученные от API Кинопоиска,
    в объекты класса Movie
    """
    result_lst = list()
    for i_dict in lst:
        movie = Movie(id_movie=i_dict['id'],
                      name=i_dict['name'],
                      year=i_dict['year'],
                      country=', '.join(list(map(lambda x: x['name'], i_dict['countries']))),
                      genre=', '.join(list(map(lambda x: x['name'], i_dict['genres']))),
                      rating_kp=i_dict['rating']['kp'],
                      rating_imdb=i_dict['rating']['imdb'],
                      description=i_dict['description'] if i_dict['description'] else 'не найдено',
                      poster_url=i_dict['poster']['url'] if i_dict['poster']['url'] else 'не найден')
        result_lst.append(movie)

    return result_lst
