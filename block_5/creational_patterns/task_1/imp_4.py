import random
import uuid
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from queue import Empty
from queue import LifoQueue


class CellPrototype(ABC):
    @abstractmethod
    def clone(self):
        pass


@dataclass
class Cell(CellPrototype):
    """Клетка - обьект игры."""

    color: tuple = (0, 0, 0)
    name: uuid.UUID = uuid.uuid4()
    size: int = random.randint(1, 10)

    def clone(self):
        new = self.__class__(self.color, self.name, self.size)
        new.__dict__.update(self.__dict__)

        return new


class PoolCell:
    """Клеточный пул."""

    def __init__(self):
        self.queue = LifoQueue()
        self.etalon_cell = Cell()

    def get(self):
        """Получение клетки из пула.

        :return: полученная клетка
        """
        try:
            cell = self.queue.get_nowait()
        except Empty:
            cell = self.etalon_cell.clone()
            cell.color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        return cell

    def release(self, cell):
        """Возврат клетки в пул.

        :param cell: возвращаемая клетка
        """
        self.queue.put(cell)

    def size(self):
        """Текущий размер пула."""
        return self.queue.qsize()


class LiveGame:
    """Класс игры ЖИЗНЬ."""

    def __init__(self, pool):
        """Инициализация класса.

        :param pool: пул с клетками
        """
        self.pool = pool

    def give_birth_cell(self):
        """Породить новую клетку.

        :return: новорожденная клетка
        """
        cell = self.pool.get()
        print(cell)
        return cell

    def kill_cell(self, cell):
        """Убиваваем клетку.

        :param cell: клетка, которую нужно убить
        """
        self.pool.release(cell)