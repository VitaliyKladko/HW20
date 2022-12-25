import pytest
from unittest.mock import MagicMock

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService


# готовим фикстуру durector_dao
@pytest.fixture()
def director_dao_fixture():
    """
    Подготавливает данные, которые для нас генерит DAO
    :return: мокнутый director_dao
    """
    # это обычно расп. в файле implemented.py(контейнер)
    director_dao = DirectorDAO(None)

    # создаем режисеров с помощью моделей
    vitaliy = Director(id=1, name='Vitaliy')
    dima = Director(id=2, name='Dima')

    # мокаем(эмулируем) методы dao
    director_dao.get_one = MagicMock(return_value=vitaliy)
    director_dao.get_all = MagicMock(return_value=[vitaliy, dima])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    # фикстура отдает мокнутый экземпляр DirectorDAO
    return director_dao


# тесты Director_Service
class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao_fixture):
        self.director_service = DirectorService(dao=director_dao_fixture)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) == 2

    def test_create(self):
        director_data = {
            'name': 'Gleb',
        }

        director = self.director_service.create(director_data)

        assert director.id == 3

    def test_update(self):
        director_data = {
            'id': 1,
            'name': 'Gleb',
        }

        self.director_service.update(director_data)

    def test_delete(self):
        self.director_service.delete(1)
