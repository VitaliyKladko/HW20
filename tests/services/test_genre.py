import pytest
from unittest.mock import MagicMock

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService


@pytest.fixture()
def genre_dao_fixture():
    genre_dao = GenreDAO(None)

    comedies = Genre(id=1, name='Comedies')
    peplum = Genre(id=2, name='Peplum')

    genre_dao.get_one = MagicMock(return_value=comedies)
    genre_dao.get_all = MagicMock(return_value=[comedies, peplum])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao_fixture):
        self.genre_service = GenreService(dao=genre_dao_fixture)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id == 1

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres) == 2

    def test_create(self):
        genre_data = {
            'name': 'action',
        }

        genre = self.genre_service.create(genre_data)

        assert genre.id == 3

    def test_update(self):
        genre_data = {
            'id': 1,
            'name': 'Military',
        }

        self.genre_service.update(genre_data)

    def test_delete(self):
        self.genre_service.delete(1)
