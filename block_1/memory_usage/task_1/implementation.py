class TempFile:

    def __init__(self, path) -> None:
        super().__init__()
        self._f = open(path, 'wb')
