import numpy as np
import pandas


def chi_aux(class_data: np.array, w: np.array) -> np.float64:
    """
    Auxiliary method to simplify the calculation of the chi squared
    :param class_data: class values
    :param w: feature values
    :return: chi squared of the feature
    """
    # cont = table(class_data, w)
    categories, cat_idx = np.unique(class_data, return_inverse=True)
    values, val_idx = np.unique(w, return_inverse=True)
    cont: np.array = np.zeros((len(categories), len(values)), dtype=np.uint64)
    np.add.at(cont, (cat_idx, val_idx), 1)

    # calculate the sum of the rows and columns
    row_sums: np.array = np.sum(cont, axis=1)
    col_sums: np.array = np.sum(cont, axis=0)
    all_sum: int = np.sum(col_sums)

    # use numpy outer to calculate the product of the sums
    expected_matrix: np.array = np.outer(row_sums, col_sums) / all_sum

    # chis = sum((cont - expected_matrix) ^ 2 / expected_matrix)
    chis: np.float64 = np.sum(np.square(cont - expected_matrix) / expected_matrix)
    if chis == 0 or len(col_sums) < 2 or len(row_sums) < 2:
        return np.float64(0)
    return np.sqrt(chis / (all_sum * min(len(col_sums) - 1, len(row_sums) - 1)))


def chi_squared(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Calculate the chi squared of the features
    :param data: dataset to calculate the chi squared of the features
    :return: chi squared of the features of the dataset
    """
    attr_names: list[str] = data.columns[1:]
    np_data: np.array = data.to_numpy(np.uint)
    np_class_data: np.array = np_data[:, 0]
    #  calculate the chi squared of the features
    np_results = np.apply_along_axis(lambda x: chi_aux(np_class_data, x), 0, np_data[:, 1:])
    return pandas.DataFrame({"attr_importance": np_results}, index=attr_names)
