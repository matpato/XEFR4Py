import unittest

import numpy as np
import pandas
from pandas.core.dtypes.common import is_integer_dtype

from eefr.discretizer.__init__ import get_data_frame_from_formula, discretize, supervised_discretization, discretize_all


class TestDiscretizer(unittest.TestCase):
    def test_get_data_frame_from_formula(self):
        data: pandas.DataFrame = pandas.DataFrame([['a'], ['c'], ['b']])
        data = get_data_frame_from_formula(data)
        self.assertTrue(is_integer_dtype(data[0]))
        self.assertEqual([0, 2, 1], data[0].tolist())

        data = pandas.DataFrame([[True], [False], [False]])
        data = get_data_frame_from_formula(data)
        self.assertTrue(is_integer_dtype(data[0]))
        self.assertEqual([1, 0, 0], data[0].tolist())

    # noinspection PyTypeChecker
    def test_discretizer(self):
        data: pandas.DataFrame = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                                   np.concatenate([np.random.random(100) * -1, np.random.random(100)])
                                                   ]).transpose()
        discretized: pandas.DataFrame = discretize(data)
        unique, count = np.unique(discretized[1], return_counts=True)
        self.assertTrue(is_integer_dtype(discretized[1]))
        self.assertEqual([0, 1], unique.tolist())
        self.assertEqual([100, 100], count.tolist())

    # noinspection PyTypeChecker
    def test_supervised_discretization(self):
        data: pandas.DataFrame = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                                   np.concatenate([np.random.random(100) * -1, np.random.random(100)]),
                                                   range(200),
                                                   np.concatenate([range(-50, 0), range(400, 500), range(50)])
                                                   ]).transpose()
        discretized: pandas.DataFrame = supervised_discretization(data)
        unique, count = np.unique(discretized[1], return_counts=True)
        self.assertTrue(is_integer_dtype(discretized[1]))
        self.assertEqual([0, 1], unique.tolist())
        self.assertEqual([100, 100], count.tolist())

        unique, count = np.unique(discretized[2], return_counts=True)
        self.assertTrue(is_integer_dtype(discretized[2]))
        self.assertEqual([0, 1], unique.tolist())
        self.assertEqual([100, 100], count.tolist())

        unique, count = np.unique(discretized[3], return_counts=True)
        self.assertTrue(is_integer_dtype(discretized[3]))
        self.assertEqual([0, 1, 2, 3], unique.tolist())
        self.assertEqual([50, 50, 50, 50], count.tolist())

    def test_discretize_all(self):
        data: pandas.DataFrame = pandas.DataFrame([range(200),
                                                   range(200)
                                                   ]).transpose()
        discretized: pandas.DataFrame = discretize_all(data)
        unique, count = np.unique(discretized[0], return_counts=True)
        self.assertTrue(is_integer_dtype(discretized[0]))
        self.assertEqual([0, 1, 2, 3, 4], unique.tolist())
        self.assertEqual([40, 40, 40, 40, 40], count.tolist())

        unique, count = np.unique(discretized[1], return_counts=True)
        self.assertTrue(is_integer_dtype(discretized[1]))
        self.assertEqual([0, 1, 2, 3, 4], unique.tolist())
        self.assertEqual([40, 40, 40, 40, 40], count.tolist())


if __name__ == '__main__':
    unittest.main()
