class EmptyPlaceDoesNotExist(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Свободное место не найдено', *args)