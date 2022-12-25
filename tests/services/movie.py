import pytest
from unittest.mock import MagicMock

from dao.model.movie import Movie
from dao.model.genre import Genre
from dao.model.director import Director
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao_fixture():
    movie_dao = MovieDAO(None)

    director_1 = Director(id=1, name='Vitaliy')
    genre_1 = Genre(id=1, name='Surrealism')

    film = Movie(
        id=1,
        title='test_title',
        description='test_description',
        trailer='test_trailer',
        year=2022,
        rating=6.7,
        genre_id=1,
        genre=genre_1,
        director_id=1,
        director=director_1
    )

    movie_dao.get_one = MagicMock(return_value=film)
    movie_dao.get_all = MagicMock(return_value=[film, ])
    movie_dao.create = MagicMock(return_value=Movie(id=10, title='test_2'))
    movie_dao.update = MagicMock()
    movie_dao.delete = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao_fixture):
        self.movie_service = MovieService(dao=movie_dao_fixture)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'test_title'

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) == 1

    def test_create(self):
        movie_data = {
            'id': 10,
            'title': 'test_2'
        }

        new_movie = self.movie_service.create(movie_data)

        assert new_movie.id == 10
        assert new_movie.title == 'test_2'

    def test_update(self):
        movie_data = {
            'id': 10,
            'title': 'test_2'
        }

        self.movie_service.update(movie_data)

    def test_delete(self):
        self.movie_service.delete(1)

    def test_partially_update(self):
        movie_data = {
            'id': 1,
            'year': 2020,
        }

        movie_to_update = self.movie_service.partially_update(movie_data)

        assert movie_to_update.year == movie_data.get('year')
