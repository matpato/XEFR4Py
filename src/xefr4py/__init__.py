import datetime
import logging
import os.path
from typing import Any

import function
import numpy as np
import pandas

from xefr4py.discretizer import get_data_frame_from_formula, discretize_all
from xefr4py.metrics import Metric
from Utils import get_log_dir

LOG_INTERVAL = datetime.timedelta(seconds=30)

LOGS_PATH: str = get_log_dir()


def _generate_log_file(data: dict[str, Any], file_name: str) -> None:
    """
    Generate a log file with the data

    :param data: data to log
    :param file_name: file name
    """
    if not os.path.exists(LOGS_PATH):
        os.makedirs(LOGS_PATH)
    pandas.DataFrame([data]).to_csv(f'{LOGS_PATH}/{file_name}.tsv', index=False, sep='\t')


def _get_n_randoms_rows_subsets(n_rows: int, size: int, iterations: int, generate_logs: bool = True) -> list[list[int]]:
    """
    Get N random row indexes subsets

    :param n_rows: dataset number of rows
    :param size: dataset partition number of rows
    :param iterations: number of partitions (N)
    :param generate_logs: generate logs for the Knowledge Viewer App, defaults to True
    :return: N dataset row indexes partitions
    """
    timer = datetime.datetime.now()

    randomRowsN: list[list[int]] = list()
    for _ in range(iterations):
        randomRowsN.append(np.random.randint(0, n_rows, size, int).tolist())

    # Log for Knowledge Viewer App
    if generate_logs:
        _generate_log_file({'Dataset Size': n_rows,
                           'Subset Size': size,
                           'Number of Subsets': iterations,
                           'Execution Time': datetime.datetime.now() - timer
                            }, 'get_n_randoms_rows_subsets')
    return randomRowsN


def _calculate_weights_sampling(Y: pandas.Series, X: pandas.DataFrame, random_rows: list[list[int]],
                                function_to_use: function, generate_logs: bool = True) -> pandas.DataFrame:
    """
    for each sample calculate feature weights based on functionTouse metrics

    :param Y: dataset class
    :param X: dataset features
    :param random_rows: N subset index rows
    :param function_to_use: statistical function to use as relevancy metric of each feature
    :param generate_logs: generate logs for the Knowledge Viewer App, default value True
    :return: N x M list of weights
    """
    f_names: list[str] = X.columns.tolist()
    dataset: pandas.DataFrame = pandas.concat([Y, X], axis=1)

    # calculate the weights
    weights: list[float] = _apply_along_columns(
        lambda x: function_to_use(dataset.iloc[x, :]).iloc[:, 0].tolist(), random_rows,
        function_to_use.__name__.replace('_', ' ')
    )

    # generate the weights data frame
    weights_data: pandas.DataFrame = pandas.DataFrame(weights, columns=f_names)

    # Log for Knowledge Viewer App
    if generate_logs:
        weights_data.to_csv(f'{LOGS_PATH}/metric_{function_to_use.__name__}.tsv', index=False, sep='\t')

    return weights_data


def _apply_along_columns(function_to_use: function, array: list[list[int]], function_name: str) -> list[float]:
    """
    Apply a function to each column of a dataset

    :param function_to_use: function to apply
    :param array: random rows indexes
    :param function_name: function name to show in the log
    :return: list of results of the function applied to each column
    """
    # calculate the time to log
    next_log: datetime = datetime.datetime.now() + LOG_INTERVAL

    ret: list[float] = list()

    # apply the function to each column
    for i in range(len(array)):
        ret.append(function_to_use(array[i]))

        # verify if it is time to log
        now = datetime.datetime.now()
        if next_log < now:
            # calculate the next time to log and log
            next_log = now + LOG_INTERVAL
            logging.info(f"{function_name}: Calculating... {round(i / len(array) * 100, 2)}%")

    return ret


def _cutoff_by_contrib(attrs: pandas.DataFrame, contrib: float = 1) -> list[str]:
    """
    Selects features with contribution > uniform contribution * contrib

    :param attrs: features weights
    :param contrib: selection factor close to 1, subsets all features with contribution > uniform contribution * contrib
    :return: list of features names, inverse ordered by its weights
    """
    # special cases
    if attrs.shape[0] == 0:
        return []
    elif attrs.shape[0] == 1:
        return list(attrs.index)

    # sort the features by its weights
    perm: list[int] = attrs.iloc[:, 0].sort_values(ascending=False).index
    attrs = attrs.loc[perm, :]

    # calculate the uniform contribution and select the features
    min_contrib: float = attrs.sum().sum() / attrs.shape[0]
    contributors: list[bool] = [attrs.iloc[idx, 0] > min_contrib * contrib for idx in range(attrs.shape[0])]

    return list(attrs.index[contributors])


def _calculate_rank_sampling(weights: pandas.DataFrame, features_names: list[str], weight_per_group: list[float],
                             cut_off: float = -1, generate_logs: bool = True) -> list[str]:
    """
    Calculate the rank of features based on the weights of each feature

    :param weights: weights of each feature
    :param features_names: features names to be ranked
    :param weight_per_group: weight per group of each rank
    :param cut_off: 0 (all features), k (k most ranked features), -1 (automatic k calculation)
    :param generate_logs: generate logs for the Knowledge Viewer App, default value True
    :return: rank subset of features ordered by its relevance
    """
    # calculate the time to log
    next_log = datetime.datetime.now() + LOG_INTERVAL

    # create the rank data frame
    weight_col = "Weight"
    rank: pandas.DataFrame = pandas.DataFrame(index=features_names, columns=[weight_col])
    rank[weight_col] = 0.0

    # calculate the rank
    for i in range(len(weights)):
        aux_t: pandas.DataFrame = pandas.DataFrame(weights.iloc[i, :]).T
        aux_t = aux_t.sample(frac=1)
        aux: list[str] = aux_t.iloc[0, :].sort_values(ascending=False).index.tolist()
        for j in range(len(aux)):
            rank.loc[aux[j], weight_col] += weight_per_group[j]

        # verify if it is time to log
        now = datetime.datetime.now()
        if next_log < now:
            # calculate the next time to log and log
            next_log += LOG_INTERVAL
            logging.info(f"{i / len(weights) * 100}% Calculating rank...")

    ret: list[str]
    if cut_off == -1:
        # automatic best k calculation
        logging.info("Automatic best k calculation...")
        ret = _cutoff_by_contrib(rank, 0.99)
    else:
        # select the best k
        logging.info("Calculating k best columns...")
        if cut_off > rank.shape[0] or cut_off < 1:
            cut_off = rank.shape[0]
        ret = rank[weight_col].sort_values(ascending=False).index.tolist()[:cut_off]

    # prepare the rank data frame to log
    rank_data: pandas.DataFrame = rank.T[ret]

    # Log for Knowledge Viewer App
    if generate_logs:
        rank_data.to_csv(f'{LOGS_PATH}/rank_sampling.tsv', index=False, sep='\t')

    return ret


class EEFR:
    """
    Enhanced Ensemble Features Ranking class that builds the object to calculate the features ranking with
    method ensemble_features_ranking
    """
    __Y: pandas.Series
    __X: pandas.DataFrame

    __generate_logs: bool

    def __init__(self, dataset: pandas.DataFrame, class_column: str = None, blacklist_columns: list[str] = None,
                 generate_logs: bool = True):
        """
        Takes a dataset to process

        :param dataset: dataset to process
        :param class_column: class column name
        :param blacklist_columns: list of columns to ignore
        """
        # timer for Knowledge Viewer App logs
        constructor_timer = datetime.datetime.now()

        # logging configuration for the algorithm
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)
        logging.captureWarnings(True)

        # dataset processing
        if class_column is None:
            class_column = dataset.columns[0]
        if blacklist_columns is None:
            blacklist_columns = []
        blacklist_columns.append(class_column)

        self.__Y = dataset[class_column]
        self.__X = dataset.drop(columns=blacklist_columns)
        self.__generate_logs = generate_logs

        if os.path.exists(LOGS_PATH):
            for file in os.listdir(LOGS_PATH):
                os.remove(os.path.join(LOGS_PATH, file))

        logging.info("Dataset loaded")
        logging.info("Starting Discretization...")

        # timer for the Knowledge Viewer App log
        discretizer_timer = datetime.datetime.now()

        # prepare the dataset for the discretization and discretize it
        new_data = pandas.concat([self.__Y, self.__X], axis=1)
        new_data = get_data_frame_from_formula(new_data)
        new_data = discretize_all(new_data)

        # pause the timer for the Knowledge Viewer App log
        discretizer_timer = datetime.datetime.now() - discretizer_timer

        logging.info("Discretization done")

        # update the dataset with the discretized data
        self.__Y = new_data.iloc[:, 0]
        self.__X = new_data.iloc[:, 1:]

        # calculate the class distribution and log it
        unique, counts = np.unique(self.__Y.to_numpy(), return_counts=True)

        if self.__generate_logs:
            _generate_log_file({'Classes': unique,
                               'Classes Distribution': counts,
                               'Total Removed Instances': dataset.shape[0] - self.__X.shape[0],
                               'Execution Time': discretizer_timer
                                }, 'discretizer')

            _generate_log_file({'Class Column': class_column,
                               'Blacklist Columns': blacklist_columns[:-1],
                               'Total Instances': self.__X.shape[0],
                               'Total Features': self.__X.shape[1],
                               'Execution Time': datetime.datetime.now() - constructor_timer
                                }, 'constructor')

    def ensemble_features_ranking(self, n_rows: int = None, n_tries: int = 10, cut_off: int = -1,
                                  methods: list[Metric] = None) -> list[str]:
        """
        Outputs a features name list inversely ordered by relevance

        :param n_rows: number of rows per subset, default value 10
        :param n_tries: number of subsets, default value dataset rows/2
        :param cut_off: 0 (all features), k (k most ranked features), -1 (automatic k calculation), default value -1
        :param methods: list of metrics to use, default value (gain_ratio, symmetrical_uncertainty, chi_squared, random_forest_importance)
        :return: list of features names, inverse ordered by its weights
        """
        # timer for Knowledge Viewer App log
        eefr_timer = datetime.datetime.now()

        # process the parameters to use the default values
        if methods is None:
            methods = [Metric.GAIN_RATIO, Metric.SYMMETRICAL_UNCERTAINTY, Metric.CHI_SQUARED,
                       Metric.RANDOM_FOREST_IMPORTANCE]
        if n_rows is None:
            n_rows = int(self.get_total_instances() / 2)

        random_rows_n: list[list[int]] = _get_n_randoms_rows_subsets(self.get_total_instances(), n_rows, n_tries,
                                                                     self.__generate_logs)
        n: int = self.get_total_features()

        logging.info(f"The Dataset as {self.get_total_instances()} lines and {n} columns")

        # calculate the weight per group
        weight_per_group: [int] = range(n, 0, -1)
        weight_per_group = [int(w * (w ** 0.5) / (n ** 0.5)) for w in weight_per_group]

        logging.info("Starting Weights calculation...")

        # timer for Knowledge Viewer App log
        metrics_timer = datetime.datetime.now()

        weights: list[pandas.DataFrame] = list()
        for i in range(len(methods)):
            method: Metric = methods[i]
            # timer for Knowledge Viewer App log
            method_timer = datetime.datetime.now()
            logging.info(
                f"Calculating weights for metric: {method.__name__.replace('_', ' ')} ({i + 1}/{len(methods)})")
            weights.append(_calculate_weights_sampling(self.__Y, self.__X, random_rows_n, method, self.__generate_logs))

            # Log for Knowledge Viewer App
            if self.__generate_logs:
                _generate_log_file({'Execution Time': datetime.datetime.now() - method_timer},
                                   method.__name__)

        # Log for Knowledge Viewer App
        if self.__generate_logs:
            _generate_log_file({'Metrics': [method.__name__.replace('_', ' ') for method in methods],
                               'Execution Time': datetime.datetime.now() - metrics_timer},
                              'calculate_weights_sampling')

        logging.info("Concatenating the weights...")

        # concatenate the weights into a data frame
        weights_list: pandas.DataFrame = pandas.concat(weights, ignore_index=True)
        features_names: list[str] = self.__X.columns

        logging.info("Starting rank calculation...")

        # timer for Knowledge Viewer App log
        rank_timer = datetime.datetime.now()

        ret: list[str] = _calculate_rank_sampling(weights_list, features_names, weight_per_group, cut_off,
                                                  self.__generate_logs)

        # Logs for Knowledge Viewer App
        if self.__generate_logs:
            _generate_log_file({'Total Features': self.__X.shape[1],
                               'Selected Count': len(ret),
                               'Execution Time': datetime.datetime.now() - rank_timer}, 'calculate_rank_sampling')

            _generate_log_file({'Execution Time': datetime.datetime.now() - eefr_timer}, 'EEFR')

        logging.info("Done!")
        return ret

    def get_total_features(self):
        """
        Get the number of features of the dataset

        :return: number of features of the dataset
        """
        return self.__X.shape[1]

    def get_total_instances(self):
        """
        Get the number of instances of the dataset

        :return: number of instances of the dataset
        """
        return self.__X.shape[0]
