import pandas
from sklearn.ensemble import RandomForestRegressor


def r_forest_importance2(dataset: pandas.DataFrame) -> pandas.DataFrame:
    """
    Returns the importance of de features based on the random forest regressor

    :param dataset: dataset that wants to calculate the importance of the features
    :return: importance of the features
    """
    rf: RandomForestRegressor = RandomForestRegressor()
    rf.fit(dataset.iloc[:, 1:], dataset[dataset.columns[0]])
    return pandas.DataFrame({"attr_importance": rf.feature_importances_}, index=dataset.columns[1:])
