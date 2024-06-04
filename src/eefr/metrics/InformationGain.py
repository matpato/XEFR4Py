from enum import Enum

import numpy as np
import pandas
from scipy.stats import entropy


class InformationGain(Enum):
    """
    Enum to define the information gain methods
    """
    GAIN_RATIO = "gainratio"
    SYMMETRICAL_UNCERTAINTY = "symuncert"


def entropy_helper(x: np.array) -> float:
    """
    Calculates the entropy of the column.
    :param x: column or table to calculate the entropy
    :return: entropy of the column
    """
    if len(x.shape) == 2:
        # Create a contingency table
        features, fet_idx = np.unique(x[:, 0], return_inverse=True)
        values, val_idx = np.unique(x[:, 1], return_inverse=True)
        cont: np.array = np.zeros((len(features), len(values)), dtype=np.uint64)
        np.add.at(cont, (fet_idx, val_idx), 1)

        # Flatten the table to a 1D array
        table = cont.flatten()
    else:
        table = np.unique(x, return_counts=True)[1]
    return entropy(table)


def information_gain_body(data: pandas.DataFrame, metric: InformationGain) -> pandas.DataFrame:
    """
    Auxiliary method for the information gain methods
    :param data: dataset to calculate the metric
    :param metric: specify the information metric
    :return: return a dataset with the attribute importance
    """
    attr_names: [str] = data.columns[1:]
    data: np.array = data.to_numpy(dtype=np.uint)
    attr_entropies: np.array = np.apply_along_axis(entropy_helper, 0, data)
    # noinspection PyTypeChecker
    class_entropy: float = attr_entropies[0]
    attr_entropies = attr_entropies[1:]
    class_data: np.array = data[:, 0]
    joint_entropies: np.array = np.apply_along_axis(lambda x: entropy_helper(np.array([class_data, x]).transpose()),
                                                    0, data[:, 1:])
    results: np.array = class_entropy + attr_entropies - joint_entropies
    if metric == InformationGain.GAIN_RATIO:
        # can't use numpy.where because of division by 0
        non_zero_mask: np.array = attr_entropies != 0
        results[non_zero_mask] = np.divide(results[non_zero_mask], attr_entropies[non_zero_mask])
        results[~non_zero_mask] = 0
    elif metric == InformationGain.SYMMETRICAL_UNCERTAINTY:
        results = 2 * results / (attr_entropies + class_entropy)
    return pandas.DataFrame({"attr_importance": results}, index=attr_names)


def gain_ratio(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Calculate the gain ratio for the dataset
    :param data: dataset to use
    :return: gain ratio of the dataset
    """
    return information_gain_body(data, metric=InformationGain.GAIN_RATIO)


def symmetrical_uncertainty(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Calculate the symmetrical uncertainty for the dataset
    :param data: dataset to use
    :return: symmetrical uncertainty of the dataset
    """
    return information_gain_body(data, metric=InformationGain.SYMMETRICAL_UNCERTAINTY)
