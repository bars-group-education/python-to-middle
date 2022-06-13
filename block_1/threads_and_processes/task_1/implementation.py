import time
import uuid
from multiprocessing import Process, Queue


class Front:

    def __init__(self) -> None:
        super().__init__()
        self._worker = None
        self._messages = Queue()

    def get_result(self, id_):
        pass

    def call_command(self, command_name, params):
        id_ = uuid.uuid4()
        self._messages.put((id_, command_name, params))

        return id_

    def start(self):
        self._worker = Process(target=self._run, args=(self._messages,))
        self._worker.start()

    def stop(self):
        self._worker.terminate()
        self._worker.join()

    @staticmethod
    def _run(messages):
        while True:
            message = messages.get()
            if message:
                pass

            time.sleep(1.0)


class Back:

    def start(self):
        pass

    def stop(self):
        pass


class Composer:

    def __init__(self) -> None:
        super().__init__()
        self._front = Front()
        self._back = Back()

    def start(self):
        self._back.start()
        self._front.start()

    def stop(self):
        self._front.stop()
        self._back.stop()

    def get_front(self):
        return self._front