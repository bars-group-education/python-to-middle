import uuid
import time
from threading import Thread
import multiprocessing as mp


class Front:
    """Фронт."""

    def __init__(self, conn_from_front, message_with_results) -> None:
        super().__init__()
        self._perform_results_worker = None
        self._worker = None
        self._messages = mp.Queue()
        self.conn_from_front = conn_from_front
        self.message_with_results = message_with_results
        manager = mp.Manager()
        self.results = manager.dict()

    @staticmethod
    def _run(messages):
        """Опрашивает очередь с командами на обработку и
        передаёт их в трубку для бэка."""

        while True:
            message = messages.get()
            if message:
                _id, command_name, params_list, conn_from_front = message
                conn_from_front.send((_id, command_name, params_list))
            time.sleep(1.0)

    @staticmethod
    def _perform_results(message_with_results, results) -> None:
        """Получает из очереди с результатами обработки элементы и
        преобразет их в словарь."""

        while True:
            result = message_with_results.get()
            if result:
                id_, result = result
                results[id_] = result
            time.sleep(1.0)

    def start(self):
        """Запускает процессы фронта."""

        self._worker = mp.Process(
            target=self._run,
            args=(self._messages, )
        )
        self._worker.start()
        self._perform_results_worker = mp.Process(
            target=self._perform_results,
            args=(self.message_with_results, self.results)
        )
        self._perform_results_worker.start()

    def call_command(self, command_name, params_list):
        """Передаёт команду пользователя в очередь для обработки -
        пользователю возвращает уникальный идентификатор
        для дальнейшего получения результата."""

        _id = uuid.uuid4()
        self._messages.put(
            (_id, command_name, params_list, self.conn_from_front)
        )
        return _id

    def get_result(self, key):
        """В цикле опрашивает словар с результатами выполнения команд,
        если находит нужный (соответствующий ключу) - отдаёт."""

        while True:
            result = self.results.get(key, False)

            if result is not False:
                return result
            time.sleep(1.0)

    def stop(self):
        """Останавливает все процессы фронта."""

        self._worker.terminate()
        self._worker.join()
        self._perform_results_worker.terminate()
        self._perform_results_worker.join()


class Back:
    """Бэк."""

    def __init__(self, link_to_back, message_with_results):
        super().__init__()
        self._worker = None
        self.link_to_back = link_to_back
        self.message_with_results = message_with_results

    def start(self):
        """Запускает процесс бэка."""

        self._worker = mp.Process(target=self._run)
        self._worker.start()

    def _perform(self, id_, command_name, params_list) -> None:
        """Распознаёт команду и применяет её к переданным параметрам,
        результат помещает в очередь."""

        result = None

        if command_name == 'sum':
            result = sum(params_list)
        elif command_name == 'min':
            result = min(params_list)
        elif command_name == 'max':
            result = max(params_list)
        self.message_with_results.put((id_, result))

    def _run(self) -> None:
        """Получает от фронта команды и параметры по трубке и
        запускает их исполнение в отдельных потоках,
        если пришла неизвестная команда - сразу передаёт в очередь None."""

        while True:
            message = self.link_to_back.recv()
            if message:
                id_, command_name, params_list = message
                if command_name in ('sum', 'max', 'min'):
                    thread = Thread(
                        target=self._perform,
                        args=(id_, command_name, params_list)
                    )
                    thread.start()
                    thread.join()
                else:
                    self.message_with_results.put((id_, None))
            time.sleep(1.0)

    def stop(self):
        """Останавливает все процессы бэка."""

        self._worker.terminate()
        self._worker.join()


class Composer:
    """Компоновщик бэка и фронта."""

    def __init__(self) -> None:

        link_from_front, link_to_back = mp.Pipe()
        message_with_results = mp.Queue()
        self._front = Front(link_from_front, message_with_results)
        self._back = Back(link_to_back, message_with_results)

    def get_front(self):
        """Возвращает фронт."""

        return self._front

    def start(self):
        """Запускает компоновщик."""

        self._back.start()
        self._front.start()

    def stop(self):
        """Останавливает компоновщик."""

        self._back.stop()
        self._front.stop()
