from copy import deepcopy
from dataclasses import dataclass
import uuid
import random
from queue import LifoQueue, Empty
# если нужно, импортируйте дополнительные модули


@dataclass
class Cell:
    """Клетка - обьект игры"""
    color: tuple = (0, 0, 0)
    name: str = uuid.uuid4()
    size: int = random.randint(1, 10)

    def clone(self):
        return deepcopy(self)


class PoolCell:
    """Клеточный пул"""

    def __init__(self):
        self.queue = LifoQueue()
        self.etalon_cell = Cell()

    def get(self):
        """
            Получение клетки из пула
        :return: полученная клетка
        """
        try:
            cell = self.queue.get_nowait()
        except Empty:
            # добавьте свой код сюда - необходимо скопировать эталлонную ячейку self.etalon_cell
            cell = self.etalon_cell.clone()
            cell.color = lambda: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        return cell

    def release(self, cell):
        """
            Возврат клетки в пул
        :param cell: возвращаемая клетка
        """
        self.queue.put(cell)

        return self

    def size(self):
        """Текущий размер пула"""
        return self.queue.qsize()


class LiveGame:
    """ Класс игры ЖИЗНЬ """

    def __init__(self, pool):
        """
            Инициализация класса
        :param pool: пул с клетками
        """
        self.pool = pool

    def give_birth_cell(self):
        """
            Породить новую клетку
        :return: новорожденная клетка
        """
        return self.pool.get()

    def kill_cell(self, cell):
        """
            Убиваваем клетку
        :param cell: клетка, которую нужно убить
        """
        self.pool.release(cell)
