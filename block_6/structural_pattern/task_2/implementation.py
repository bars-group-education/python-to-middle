class CarException(Exception):
    """Исключение, связанное с неправильным использованием автомобиля"""
    pass


class Car:
    """Автомобиль как сложная система"""
    def __init__(self):
        """Инициализация состояния автомобиля"""
        self.state = {
            'open_car': False,
            'moving': False,
            'engine_work': False
        }

    def open(self):
        """Открыть ключем автомобиль"""
        self.state['open_car'] = True

    def close(self):
        """Закрыть ключем автомобиль"""
        if self.state['moving']:
            raise CarException('Нельзя закрыть движущийся автомобиль')

        if self.state['engine_work']:
            raise CarException('Двигатель автомобиля работает')

        self.state['open_car'] = False

    def start_moving(self):
        """Начать движение"""
        if not self.state['open_car']:
            raise CarException('Сначала автомобиль нужно открыть')

        if not self.state['engine_work']:
            raise CarException('Сначала нужно завести двигатель')

        self.state['moving'] = True

    def stop_moving(self):
        """Остановить движение"""
        self.state['moving'] = False

    def start_engine(self):
        """Запустить двигатель автомобиля"""
        if not self.state['open_car']:
            raise CarException('Сначала автомобиль нужно открыть')

        self.state['engine_work'] = True

    def stop_engine(self):
        """Остановить двигатель автомобиля"""
        if not self.state['open_car']:
            raise CarException('Сначала автомобиль нужно открыть')

        self.state['engine_work'] = False


class CarCommand:

    def __init__(self, car) -> None:
        super().__init__()
        self.car = car

    def do(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


class KeyCommand(CarCommand):

    def do(self):
        self.car.open()

    def undo(self):
        self.car.close()


class EngineCommand(CarCommand):

    def do(self):
        self.car.start_engine()

    def undo(self):
        self.car.stop_engine()


class MoveCommand(CarCommand):

    def do(self):
        self.car.start_moving()

    def undo(self):
        self.car.stop_moving()


class DriveCommand(CarCommand):

    def __init__(self, car) -> None:
        super().__init__(car)
        self.commands = (
            KeyCommand(self.car),
            EngineCommand(self.car),
            MoveCommand(self.car),
        )

    def do(self):
        for command in self.commands:
            command.do()

    def undo(self):
        for command in reversed(self.commands):
            command.undo()


class Driver:
    """Водитель автомобиля"""

    def __init__(self):
        self.car = Car()
        self.command = DriveCommand(self.car)

    def start_use(self):
        """Начать использование автомобиля как средства передвижения"""
        # нужно добавить свой код сюда, напишите правильную последовательность действий

        self.command.do()

    def stop_use(self):
        """Прекратить использование автомобиля"""
        # нужно добавить свой код сюда, напишите правильную последовательность действий

        self.command.undo()
