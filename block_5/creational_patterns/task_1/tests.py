import unittest

from block_5.creational_patterns.task_1.implementation import PoolCell, LiveGame


class MyTestCase(unittest.TestCase):

    def test_cell_request_100(self):
        pool = PoolCell()
        game = LiveGame(pool)
        for i in range(0, 100):
            game.give_birth_cell()

        self.assertEqual(pool.size(), 0)

    def test_cell_request_and_free(self):
        pool = PoolCell()
        game = LiveGame(pool)
        for i in range(0, 200):
            cell = game.give_birth_cell()
            game.kill_cell(cell)

        self.assertEqual(pool.size(), 1)


if __name__ == '__main__':
    unittest.main()
