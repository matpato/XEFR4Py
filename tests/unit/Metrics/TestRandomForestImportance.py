import unittest

import numpy as np
import pandas

from eefr.metrics import r_forest_importance2


class TestRandomForestImportance(unittest.TestCase):

    # noinspection PyTypeChecker
    def test_r_forest_importance2(self):
        shuffled: np.array = np.concatenate([[i for _ in range(25)] for i in range(8)])
        np.random.shuffle(shuffled)
        data: pandas.DataFrame = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                                   np.concatenate([[0 for _ in range(100)], [10 for _ in range(100)]]),
                                                   shuffled
                                                   ]).transpose()
        importance: pandas.DataFrame = r_forest_importance2(data)
        self.assertEqual(1, importance.iloc[0, 0])
        self.assertEqual(0, importance.iloc[1, 0])

        data = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                 np.concatenate([[i for _ in range(25)] for i in range(8)]),
                                 shuffled
                                 ]).transpose()
        importance = r_forest_importance2(data)
        self.assertEqual(1, importance.iloc[0, 0])
        self.assertEqual(0, importance.iloc[1, 0])


if __name__ == '__main__':
    unittest.main()
