import abc
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod


@dataclass
class Animal:
    """Абстрактное животное"""
    name: str = ''  # имя
    legs_count: int = 0  # количество ног
    wing_exist: bool = False  # флаг, есть ли крылья или нет
    roar: str = None  # рев


class BuilderAnimal(metaclass=abc.ABCMeta):
    """Абстрактный построитель животных"""
    def __init__(self):
        self._animal = Animal()
        self._is_built = False

    @abstractmethod
    def set_name(self):
        """Назначим имя животному"""
        pass

    @abstractmethod
    def set_legs_count(self):
        """Установим количество ног"""
        pass

    @abstractmethod
    def set_wing_exit(self):
        """Отметим, есть крылья или нет"""
        pass

    def set_roar(self):
        """Установим, может ли животное говорить и что оно говорит"""
        return self

    def _build(self):
        self.set_name().set_legs_count().set_wing_exit().set_roar()

    @property
    def animal(self):
        """Получение животного"""
        if not self._is_built:
            self._build()

        return self._animal


class CatBuilder(BuilderAnimal):
    """Создание кошки"""
    def set_name(self):
        self._animal.name = 'cat'

        return self

    def set_legs_count(self):
        self._animal.legs_count = 4

        return self

    def set_wing_exit(self):
        self._animal.wing_exist = False

        return self

    def set_roar(self):
        self._animal.roar = 'meow'

        return self


class CuckooBuilder(BuilderAnimal):
    """Создание кукушки"""

    def set_name(self):
        self._animal.name = 'cuckoo'

        return self

    def set_legs_count(self):
        self._animal.legs_count = 2

        return self

    def set_wing_exit(self):
        self._animal.wing_exist = True

        return self

    def set_roar(self):
        self._animal.roar = 'cucu'

        return self


class FishBuilder(BuilderAnimal):
    """Создание рыбы"""

    def set_name(self):
        self._animal.name = 'fish'

        return self

    def set_legs_count(self):
        self._animal.legs_count = 0

        return self

    def set_wing_exit(self):
        self._animal.wing_exist = False

        return self

    def set_roar(self):
        self._animal.roar = None

        return self


class ZooOwner:
    """Владелец зоопарка"""
    @staticmethod
    def create_animal(builder: BuilderAnimal):
        """
            Создание животного с помощью конкретного билдера
        :param builder: билдер
        :return:
        """
        return builder.animal
