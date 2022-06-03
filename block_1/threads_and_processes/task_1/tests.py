from unittest import (
    TestCase,
)


class Test(TestCase):

    def setUp(self) -> None:
        super().setUp()

        import multiprocessing
        from multiprocessing import Process

        class CustomProcess(Process):
            _init_count = 0

            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self.__class__._init_count += 1

        multiprocessing.Process = self.Process = CustomProcess

        import threading
        from threading import Thread

        class CustomThread(Thread):
            _init_count = 0

            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self.__class__._init_count += 1

        threading.Thread = self.Thread = CustomThread

        from block_1.threads_and_processes.task_1.implementation import Composer

        self.Composer = Composer

    def _get_front(self):
        composer = self.Composer()
        composer.start()
        front = composer.get_front()

        return front

    def test_sum(self):
        front = self._get_front()
        result = front.get_result(front.call_command('sum', [1, 2, 3]))

        self.assertEqual(result, 6)
        self.assertGreaterEqual(self.Process._init_count, 2)
        self.assertGreaterEqual(self.Thread._init_count, 1)

        self.composer.stop()

    def test_max(self):
        front = self._get_front()
        result = front.get_result(front.call_command('max', [1, 2, 3]))

        self.assertEqual(result, 3)
        self.assertGreaterEqual(self.Process._init_count, 2)
        self.assertGreaterEqual(self.Thread._init_count, 1)

        self.composer.stop()

    def test_min(self):
        front = self._get_front()
        result = front.get_result(front.call_command('min', [1, 2, 3]))

        self.assertEqual(result, 1)
        self.assertGreaterEqual(self.Process._init_count, 2)
        self.assertGreaterEqual(self.Thread._init_count, 1)

        self.composer.stop()

    def test_two_commands(self):
        front = self._get_front()

        command_max = front.call_command('max', [1, 2, 3])
        command_min = front.call_command('min', [1, 2, 3])

        result_min = front.get_result(command_min)
        result_max = front.get_result(command_max)

        self.assertEqual(result_min, 1)
        self.assertEqual(result_max, 3)
        self.assertGreaterEqual(self.Process._init_count, 2)
        self.assertGreaterEqual(self.Thread._init_count, 2)

        self.composer.stop()

    def test_unknown_command(self):
        front = self._get_front()

        result = front.get_result(front.call_command('bad', [1, 2, 3]))

        self.assertEqual(result, None)
        self.assertGreaterEqual(self.Process._init_count, 2)
        self.assertGreaterEqual(self.Thread._init_count, 1)

        self.composer.stop()
