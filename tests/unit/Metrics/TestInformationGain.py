import unittest

import numpy as np
import pandas

from xefr4py.metrics.InformationGain import entropy_helper, gain_ratio, symmetrical_uncertainty


class TestInformationGain(unittest.TestCase):
    def test_entropy(self):
        entropy: float = entropy_helper(np.array([1, 2]))
        self.assertEqual(entropy, 0.6931471805599453)

        entropy = entropy_helper(np.array([1, 2, 3, 4]))
        self.assertEqual(entropy, 1.3862943611198906)

        entropy = entropy_helper(np.array([1, 2, 3, 4, 5, 6, 7, 8]))
        self.assertEqual(entropy, 2.0794415416798357)

        entropy = entropy_helper(np.array([1, 2, 2, 1]))
        self.assertEqual(entropy, 0.6931471805599453)

        entropy = entropy_helper(np.array([1, 1, 1, 1]))
        self.assertEqual(entropy, 0)

        entropy = entropy_helper(np.array([1, 2, 1, 1]))
        self.assertEqual(entropy, 0.5623351446188083)

        entropy = entropy_helper(np.array([1, 1, 1, 1, 2, 2, 3, 4]))
        self.assertEqual(entropy, 1.2130075659799042)

        entropy = entropy_helper(np.array([1, 1, 1, 1, 1, 1, 2, 3]))
        self.assertEqual(entropy, 0.7356219397587946)

    # noinspection PyTypeChecker
    def test_gain_ratio(self):
        data: pandas.DataFrame = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                                   np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]])
                                                   ]).transpose()
        ratio: pandas.DataFrame = gain_ratio(data)
        self.assertEqual(ratio.iloc[0, 0], 1)

        data = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                 [0 for _ in range(200)]
                                 ]).transpose()
        ratio = gain_ratio(data)
        self.assertEqual(ratio.iloc[0, 0], 0)

        data = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                 np.random.randint(0, 20 + 1, 200)
                                 ]).transpose()
        ratio = gain_ratio(data)
        self.assertLess(ratio.iloc[0, 0], 0.5)

    # noinspection PyTypeChecker
    def test_symmetrical_uncertainty(self):
        data: pandas.DataFrame = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                                   np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]])
                                                   ]).transpose()
        sym: pandas.DataFrame = symmetrical_uncertainty(data)
        self.assertEqual(sym.iloc[0, 0], 1)

        data = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                 range(200)
                                 ]).transpose()
        sym = symmetrical_uncertainty(data)
        self.assertEqual(sym.iloc[0, 0], 0.23137821315975918)

        data = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                 [0 for _ in range(200)]
                                 ]).transpose()
        sym = symmetrical_uncertainty(data)
        self.assertEqual(sym.iloc[0, 0], 0.0)

        data = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                 np.concatenate([[-10 for _ in range(50)], np.random.random(150) * 10])
                                 ]).transpose()
        sym = symmetrical_uncertainty(data)
        self.assertLess(sym.iloc[0, 0], 0.5)


if __name__ == '__main__':
    unittest.main()
