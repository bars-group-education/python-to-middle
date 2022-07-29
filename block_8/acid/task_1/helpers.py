class BadConnectionEmulator:

    def __init__(self, generator) -> None:
        super().__init__()
        self.generator = generator

    def test(self):
        if not self.generator:
            raise BadConnectionEmulator


emulator = None


def set_emulator(generator):
    global emulator
    emulator = BadConnectionEmulator(generator)


class Generator:

    def __bool__(self):
        raise NotImplementedError


class TrueGenerator(Generator):

    def __bool__(self):
        return True


class SwitchGenerator(Generator):

    def __init__(self) -> None:
        super().__init__()
        self._switch = False

    def __bool__(self):
        self._switch = not self._switch

        return self._switch


class FalseGenerator(Generator):

    def __bool__(self):
        return False
