import function
import pandas
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QTableView, QSizePolicy, QSpacerItem
from pandas import DataFrame

from eefr.knowledge_viewer.Page.ChildPage import ChildPage
from eefr.knowledge_viewer.PandasTableView import PandasTableView
from Utils import get_list_from_str

"""
This class is a child page that displays the results of the weights sampling calculation.
It displays a table with the results and a button for each metric to display the diagram.
"""


# File path to get the data to display
LOG_DIR: str = '../../logs/'
FILE: str = f'{LOG_DIR}/calculate_weights_sampling.tsv'


class CalculateWeightsSamplingPage(ChildPage):
    _table_info: QTableView

    # List of buttons for each metric
    _metrics: list[QPushButton]

    def __init__(self, font: QFont, margins: QMargins, button_parent_func: function) -> None:
        super().__init__(font, margins, 'Calculate Weights Sampling', button_parent_func)

        # Load the data
        info: DataFrame = pandas.read_csv(FILE, sep='\t')

        # Get the metrics names
        metrics_names: list[str] = get_list_from_str(info['Metrics'][0])

        self._metrics = []

        # Create the buttons for the metrics
        for i in range(len(metrics_names)):
            self._metrics.append(QPushButton(metrics_names[i], self))
            self._metrics[i].setFont(font)
            self._layout.insertWidget(i + 1, self._metrics[i])

        # Remove the metrics column
        info.drop(columns='Metrics', inplace=True)

        # Create the table and add it to the layout
        self._table_info = PandasTableView(self, info.T, font)
        self._layout.insertWidget(1, self._table_info)

        # Add a spacer to the layout to keep things in place
        self._layout.insertItem(2, QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def inject_funcs(self, funcs: list[function]) -> None:
        """
        Inject the functions to navigate to the metrics.
        :param funcs: functions to be injected
        :return: None
        """
        for i in range(len(self._metrics)):
            self._metrics[i].clicked.connect(funcs[i])
