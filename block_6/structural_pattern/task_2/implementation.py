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


class Driver:
    """Водитель автомобиля"""

    def __init__(self):
        self.car = Car()

    def start_use(self):
        """Начать использование автомобиля как средства передвижения"""
        # нужно добавить свой код сюда, напишите правильную последовательность действий

    def stop_use(self):
        """Прекратить использование автомобиля"""
        # нужно добавить свой код сюда, напишите правильную последовательность действий
