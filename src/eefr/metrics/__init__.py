from enum import Enum

from eefr.metrics.ChiSquared import chi_squared
from eefr.metrics.InformationGain import gain_ratio, symmetrical_uncertainty
from eefr.metrics.RandomForestImportance import r_forest_importance2


class Metric(Enum):
    """
    Enumerate with the supported metrics
    """
    GAIN_RATIO = gain_ratio
    CHI_SQUARED = chi_squared
    RANDOM_FOREST_IMPORTANCE = r_forest_importance2
    SYMMETRICAL_UNCERTAINTY = symmetrical_uncertainty
