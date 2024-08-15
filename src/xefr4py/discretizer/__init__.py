import datetime
import logging

import numpy as np
import pandas
from pandas import CategoricalDtype
from pandas.core.dtypes.common import is_bool_dtype, is_string_dtype

from xefr4py.discretizer.MDL import MDL

LOG_INTERVAL = datetime.timedelta(seconds=30)


def get_data_frame_from_formula(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Discretize non-numeric features

    :param data: dataset to discretize
    :return: discretized dataset
    """
    d: pandas.DataFrame = data.copy()
    for i in d.columns:
        if isinstance(d[i], CategoricalDtype) or is_bool_dtype(d[i]) or is_string_dtype(d[i]):
            d[i], _ = pandas.factorize(d[i], sort=True)
    return d


def discretize(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Discretize numeric features

    :param data: dataset to discretize
    :return: discretized dataset
    """
    columns: list[str] = data.columns
    next_log: datetime = datetime.datetime.now() + LOG_INTERVAL
    for i in range(1, data.shape[1]):
        now = datetime.datetime.now()
        if next_log < now:
            next_log = now + LOG_INTERVAL
            logging.info(f"Discretizing... {round(i / len(columns) * 100, 2)}%")
        cut_points = MDL(data[columns[i]].tolist(), data[columns[0]].tolist())
        data[columns[i]] = pandas.cut(data[columns[i]], cut_points, labels=False)
    return data


def supervised_discretization(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    supervised discretization of the features, removing tuples that don't have class

    :param data: dataset to discretize
    :return: discretized dataset without missing class values
    """
    complete: pandas.Series = data.iloc[:, 0].notna()
    all_complete: bool = complete.all()
    if not all_complete:
        new_data = data[complete]
        return discretize(new_data)
    else:
        return discretize(data)


def discretize_all(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Discretize all columns of the dataset

    :param data: dataset to discretize
    :return: discretized numeric dataset, without missing class values
    """
    new_data: pandas.DataFrame = data.copy()
    class_col: str = data.columns[0]
    # Discretize the class column - if it's not categorical, use quantiles, otherwise use the number of classes
    if not isinstance(data[class_col], CategoricalDtype) and len(data[class_col].value_counts()) > 5:
        new_data[class_col] = pandas.qcut(data[class_col], 5, labels=False, duplicates='drop')
    else:
        n_classes = np.unique(data[class_col]).shape[0]
        new_data[class_col] = pandas.cut(data[class_col], n_classes, labels=False, duplicates='drop')
    new_data = supervised_discretization(new_data)
    return new_data
