import math

import numpy as np
import pandas

LOG2 = math.log(2)

"""
MDL - Fayyad and Irani
This implementation an implementation of the java weka supervised discretization in python.
The source code in java is available at:
https://git.cms.waikato.ac.nz/weka/weka/-/blob/main/trunk/weka/src/main/java/weka/filters/supervised/attribute/Discretize.java?ref_type=heads
https://github.com/Waikato/weka-3.8/blob/master/weka/src/main/java/weka/core/ContingencyTables.java
The source article of that discretization algorithm is available at:
https://sci2s.ugr.es/keel/pdf/algorithm/congreso/fayyad1993.pdf 
"""


def lnFunc(num: float) -> float:
    """
    Auxiliary function to calculate the entropy that calculates the Neper logarithm
    :param num: the number to calculate
    :return: the Neper log or 0 if we can't calculate the log
    """
    if num <= 0:
        return 0
    return num * math.log(num)


# def entropy(array: np.array) -> float:
#     """
#     Calculate the entropy with Neper logarithm
#     :param array: array to calculate the entropy
#     :return: entropy of the array
#     """
#     # initialize the return value and the total
#     returnValue: float = 0
#     total: float = 0
#
#     # calculate the values
#     for i in range(len(array)):
#         returnValue -= lnFunc(array[i])
#         total += array[i]
#
#     # return the entropy
#     if total == 0:
#         return 0
#     return (returnValue + lnFunc(total)) / (total * LOG2)


def entropy_conditioned_on_rows(matrix: np.array) -> float:
    """
    Calculate the conditioned entropy of the matrix
    :param matrix: matrix to calculate the conditioned entropy
    :return: conditioned entropy of the matrix
    """
    # initialize the return value and the total
    returnValue: float = 0
    total: float = 0

    # calculate the values
    for i in range(matrix.shape[0]):
        sumForRow: float = 0
        # calculate the values for the row
        for j in range(matrix.shape[1]):
            returnValue += lnFunc(matrix[i, j])
            sumForRow += matrix[i, j]
        returnValue -= lnFunc(sumForRow)
        total += sumForRow

    # return the entropy
    if total == 0:
        return 0
    return -returnValue / (total * LOG2)


# numpy versions of the entropy functions
def entropy(array: np.array) -> float:
    """
    Calculate the entropy with Neper logarithm
    :param array: array to calculate the entropy
    :return: entropy of the array
    """
    # Calculate probabilities
    total = np.sum(array)
    if total == 0:
        return 0
    probabilities = array / total

    # Calculate entropy
    nonzero_probabilities = probabilities[probabilities != 0]
    return -np.sum(nonzero_probabilities * np.log(nonzero_probabilities)) / LOG2
#
#
# def entropy_conditioned_on_rows(matrix: np.array) -> float:
#     """
#     Calculate the conditioned entropy of the matrix
#     :param matrix: matrix to calculate the conditioned entropy
#     :return: conditioned entropy of the matrix
#     """
#     # initialize the return value and the total
#     sumForRows: np.array = np.sum(matrix, axis=1)
#     total: float = np.sum(sumForRows)
#     # return the entropy
#     if total == 0:
#         return 0
#
#     # apply lnFunc for the rows
#     nonzero_rows = sumForRows[sumForRows != 0]
#     ln_rows = nonzero_rows * np.log(nonzero_rows)
#
#     # apply lnFunc for the matrix
#     nonzero_matrix = matrix[matrix != 0]
#     ln_matrix = nonzero_matrix * np.log(nonzero_matrix)
#
#     returnValue = np.sum(ln_matrix) - np.sum(ln_rows)
#
#     return -returnValue / (total * LOG2)


def E(prior_counts: np.array, best_counts: np.array, num_instances: int, num_cut_points: int) -> bool:
    """
    Verification of the cut point based on the conditions used in the source article
    :param prior_counts: original counts of the classes
    :param best_counts: best counts of the classes
    :param num_instances: number of instances
    :param num_cut_points: number of cut points
    :return: if the cut point should be accepted or not
    """
    prior_entropy: float = entropy(prior_counts)
    ent: float = entropy_conditioned_on_rows(best_counts)

    # Number of classes occurring in the set
    num_classes: int = np.sum(prior_counts > 0)

    # Number of classes occurring in the left subset
    num_classes_left: int = 0
    for i in range(best_counts[0].size):
        if best_counts[0, i] > 0:
            num_classes_left += 1

    # Number of classes occurring in the right subset
    num_classes_right: int = 0
    for i in range(best_counts[1].size):
        if best_counts[1, i] > 0:
            num_classes_right += 1

    # the entropy gain of the current split compared to the original one
    gain: float = prior_entropy - ent
    entropy_left: float = entropy(best_counts[0])
    entropy_right: float = entropy(best_counts[1])
    delta: float = math.log2((3 ** num_classes) - 2) - ((num_classes * prior_entropy) -
                                                        (num_classes_right * entropy_right) -
                                                        (num_classes_left * entropy_left))

    # Check if split is to be accepted
    return gain > (math.log2(num_cut_points) + delta) / num_instances


def cut_points_for_subset(sortedData: np.array, first: int, last_plus_one: int) -> np.array:
    """
    calculate the cut points of the passed subset
    :param sortedData: the class and attribute sorted by the attribute values
    :param first: first index of the subset to be considered
    :param last_plus_one: last index plus one of the subset to be considered
    :return: list of cut points if it contributes to entropy gain else None
    """
    # Compute number of instances in set
    num_instances: int = last_plus_one - first
    if num_instances < 2:
        return None

    # to make code less verbose
    sortedClass: np.array = sortedData[:, 0]
    sortedX: np.array = sortedData[:, 1]

    # Compute class counts
    counts: np.array = np.zeros((2, len(np.unique(sortedClass))))
    best_counts: np.array = counts.copy()

    for i in range(first, last_plus_one):
        counts[1, int(sortedClass[i])] += 1

    # Save prior counts
    prior_counts: np.array = counts[1].copy()

    # Entropy of the full set
    prior_entropy: float = entropy(prior_counts)
    best_entropy: float = prior_entropy

    current_cut_point: float = float('-inf')
    best_cut_point: float = current_cut_point
    best_index: int = -1
    num_cut_points: int = 0

    next_x: float = sortedX[first]

    # Find best entropy
    for i in range(first, last_plus_one - 1):
        counts[0, int(sortedClass[i])] += 1
        counts[1, int(sortedClass[i])] -= 1

        cur_x: float = next_x
        next_x: float = sortedX[i + 1]

        if cur_x < next_x:
            current_cut_point = (cur_x + next_x) / 2
            current_entropy = entropy_conditioned_on_rows(counts)
            if current_entropy < best_entropy:
                best_cut_point = current_cut_point
                best_entropy = current_entropy
                best_index = i
                best_counts = counts.copy()
            num_cut_points += 1

    # Checks if gain is zero
    gain: float = prior_entropy - best_entropy
    if gain <= 0:
        return None

    # Check if split is to be accepted
    if E(prior_counts, best_counts, num_instances, num_cut_points):
        # Select split points for the left and right subsets
        left: np.array = cut_points_for_subset(sortedData, first, best_index + 1)
        right: np.array = cut_points_for_subset(sortedData, best_index + 1, last_plus_one)

        cut_points: np.array

        # Merge cut points and return them
        if left is None and right is None:
            cut_points = np.array([best_cut_point])
        elif right is None:
            cut_points = np.concatenate([left, np.array([best_cut_point])])
        elif left is None:
            cut_points = np.concatenate([np.array([best_cut_point]), right])
        else:
            cut_points = np.concatenate([left, np.array([best_cut_point]), right])
        return cut_points

    return None


def MDL(x: list[float], y: list[float]) -> list[float]:
    """
    MDL - Fayyad and Irani - Supervised discretization method
    :param x: attribute to be discretized
    :param y: class to supervise the discretization
    :return: discretized attribute
    """
    # sort the attribute and class based on the attribute values
    data = pandas.DataFrame([y, x], index=["class", "x"]).transpose()
    sorted_data: np.array = data.sort_values("x", axis=0).to_numpy()

    # calculate the cut points
    aux: np.array = cut_points_for_subset(sorted_data, 0, sorted_data.shape[0])

    if aux is None:
        return [float('-inf'), float('inf')]

    return np.concatenate([np.array([float('-inf')]), aux, np.array([float('inf')])]).tolist()
