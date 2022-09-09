class TakeBookException(Exception):
    """Книгу уже забрали."""


class FreePositionException(Exception):
    """Отсутствие свободного места."""