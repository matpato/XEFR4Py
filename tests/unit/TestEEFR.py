import unittest

import numpy as np
import pandas

from xefr4py import _get_n_randoms_rows_subsets, _calculate_weights_sampling, Metric, _cutoff_by_contrib, \
    calculate_rank_sampling, EEFR


class TestEEFR(unittest.TestCase):
    def test_get_n_randoms_rows_subsets(self):
        iterations: int = 10
        nRows: int = 100
        size: int = 50
        subsets: list[list[int]] = _get_n_randoms_rows_subsets(nRows, size, iterations)
        self.assertEqual(iterations, len(subsets))
        for i in range(iterations):
            self.assertEqual(size, len(subsets[i]))
            unique: list[int] = np.unique(subsets[i]).tolist()
            self.assertGreaterEqual(len(unique), int(size / 2))
            for u in unique:
                self.assertIn(u, range(nRows))

    # noinspection PyTypeChecker
    def test_calculate_weights_sampling(self):
        shuffled: np.array = np.concatenate([[i for _ in range(25)] for i in range(8)])
        np.random.shuffle(shuffled)
        data: pandas.DataFrame = pandas.DataFrame([np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                                   np.concatenate([[0 for _ in range(100)], [1 for _ in range(100)]]),
                                                   [0 for _ in range(200)],
                                                   shuffled
                                                   ]).transpose()
        subsets: list[list[int]] = _get_n_randoms_rows_subsets(200, 100, 10)
        class_column: str = data.columns[0]
        weights: pandas.DataFrame = _calculate_weights_sampling(data[class_column], data.drop(columns=class_column),
                                                                subsets, Metric.GAIN_RATIO)
        weights_mean: list[float] = weights.mean().tolist()
        self.assertEqual(1, round(weights_mean[0], 1))
        self.assertEqual(0, weights_mean[1])
        self.assertLess(weights_mean[2], 0.5)

    # noinspection PyTypeChecker
    def test_cutoff_by_contrib(self):
        data: pandas.DataFrame = pandas.DataFrame([[1, 0, 0.6]]).transpose()
        cutoff: list[str] = _cutoff_by_contrib(data)
        self.assertEqual(cutoff, [0, 2])
        data = pandas.DataFrame([[1, 0, 0.6, 2]], columns=['a', 'b', 'c', 'd']).transpose()
        cutoff: list[str] = _cutoff_by_contrib(data)
        self.assertEqual(cutoff, ['d', 'a'])

    def test_calculate_rank_sampling(self):
        weights: pandas.DataFrame = pandas.DataFrame([[1.1, 0.7, 0.5], [1, 0.3, 1], [1.5, 0, 1], [1.3, 0, 1]],
                                                     columns=['a', 'b', 'c'])
        n: int = weights.shape[0]
        weightPerGroup: [int] = range(n, 0, -1)
        weightPerGroup = [int(x * (x ** 0.5) / (n ** 0.5)) for x in weightPerGroup]
        ranking: list[str] = calculate_rank_sampling(weights, list(weights.columns), weightPerGroup, -1)
        self.assertEqual(['a'], ranking)

        ranking = calculate_rank_sampling(weights, list(weights.columns), weightPerGroup, 0)
        self.assertEqual(['a', 'c', 'b'], ranking)

        ranking = calculate_rank_sampling(weights, list(weights.columns), weightPerGroup, 1)
        self.assertEqual(['a'], ranking)

        ranking = calculate_rank_sampling(weights, list(weights.columns), weightPerGroup, 2)
        self.assertEqual(['a', 'c'], ranking)

        ranking = calculate_rank_sampling(weights, list(weights.columns), weightPerGroup, 3)
        self.assertEqual(['a', 'c', 'b'], ranking)

        ranking = calculate_rank_sampling(weights, list(weights.columns), weightPerGroup, 5)
        self.assertEqual(['a', 'c', 'b'], ranking)

        ranking = calculate_rank_sampling(weights, list(weights.columns), weightPerGroup)
        self.assertEqual(['a'], ranking)

    def test_ensemble_features_ranking(self):
        data: pandas.DataFrame = pandas.DataFrame(np.concatenate([
            np.array([[0, 1, 1, 0, 1], [12, 1, 4, 23, 0], [7, 4, 2, 66, 1]]).transpose() for _ in range(100)
        ]), columns=['a', 'b', 'c'])
        eEFR: EEFR = EEFR(data)
        nRows: int = int(len(data) / 2)
        methods: list[Metric] = [Metric.GAIN_RATIO, Metric.CHI_SQUARED]
        features: list[str] = eEFR.ensemble_features_ranking(n_rows=nRows, n_tries=20, cut_off=-1, methods=methods)
        self.assertEqual(['b'], features)

    def test_ensemble_features_ranking_with_blacklist(self):
        data: pandas.DataFrame = pandas.DataFrame(np.concatenate([
            np.array([[0, 1, 1, 0, 1], [12, 1, 4, 23, 0], [7, 4, 2, 66, 1]]).transpose() for _ in range(100)
        ]), columns=['a', 'b', 'c'])
        eEFR: EEFR = EEFR(data, blacklist_columns=['b'])
        nRows: int = int(len(data) / 2)
        methods: list[Metric] = [Metric.GAIN_RATIO, Metric.CHI_SQUARED]
        features: list[str] = eEFR.ensemble_features_ranking(n_rows=nRows, n_tries=20, cut_off=-1, methods=methods)
        self.assertEqual(['c'], features)

    def test_ensemble_features_ranking_with_class_selection(self):
        data: pandas.DataFrame = pandas.DataFrame(np.concatenate([
            np.array([[12, 1, 4, 23, 0], [0, 1, 1, 0, 1], [7, 4, 2, 66, 1]]).transpose() for _ in range(100)
        ]), columns=['b', 'a', 'c'])
        eEFR: EEFR = EEFR(data, class_column='a')
        nRows: int = int(len(data) / 2)
        methods: list[Metric] = [Metric.GAIN_RATIO, Metric.CHI_SQUARED]
        features: list[str] = eEFR.ensemble_features_ranking(n_rows=nRows, n_tries=20, cut_off=-1, methods=methods)
        self.assertEqual(['b'], features)


if __name__ == '__main__':
    unittest.main()
