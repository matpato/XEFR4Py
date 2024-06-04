import unittest

import numpy as np
import pandas

from eefr.metrics.ChiSquared import chi_aux, chi_squared


class TestChiSquared(unittest.TestCase):
    def test_chi_aux(self):
        x = chi_aux([1, 0, 0, 1], [1, 0, 0, 1])
        self.assertEqual(1, x)

        x = chi_aux([1, 0, 0, 1], [13, 5, 3, 15])
        self.assertEqual(1, x)

        x = chi_aux([1, 0, 0, 1], [1, 2, 3, 4])
        self.assertEqual(1, x)

    # noinspection PyTypeChecker
    def test_chi_squared(self):
        data: pandas.DataFrame = pandas.DataFrame([np.concatenate([[0 for _ in range(10)], [1 for _ in range(10)]]),
                                                   np.concatenate([[0 for _ in range(10)], [1 for _ in range(10)]])
                                                   ]).transpose()
        chi: pandas.DataFrame = chi_squared(data)
        self.assertEqual(1, chi.iloc[0, 0])

        data = pandas.DataFrame([np.concatenate([[0 for _ in range(10)], [1 for _ in range(10)]]),
                                 [1 for _ in range(20)]
                                 ]).transpose()
        chi = chi_squared(data)
        self.assertEqual(0, chi.iloc[0, 0])
        t: np.array = np.concatenate([np.zeros(100), np.ones(100)])
        np.random.shuffle(t)
        data = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                 t
                                 ]).transpose()
        chi = chi_squared(data)
        self.assertLess(chi.iloc[0, 0], 0.25)


if __name__ == '__main__':
    unittest.main()
