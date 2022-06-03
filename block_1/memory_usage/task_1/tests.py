import gc
import os
import warnings
from unittest import (
    TestCase,
)
from pathlib import (
    Path,
)

from block_1.memory_usage.task_1.implementation import (
    TempFile,
)


class Test(TestCase):

    file_path = 'file.tmp'

    def tearDown(self) -> None:
        super().tearDown()
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_1(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.resetwarnings()
            warnings.simplefilter('ignore')
            warnings.simplefilter('always', ResourceWarning)

            tmp_file = TempFile(self.file_path)
            self.assertFalse('__del__' in dir(tmp_file))

            del tmp_file
            gc.collect()
            self.assertFalse(w and str(w[-1]))

            path = Path(self.file_path)
            self.assertFalse(path.exists())
