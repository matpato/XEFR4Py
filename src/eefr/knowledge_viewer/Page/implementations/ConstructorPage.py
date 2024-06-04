import function
import pandas
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QTableView, QSpacerItem, QSizePolicy
from pandas import DataFrame

from eefr.knowledge_viewer.Page.ChildPage import ChildPage
from eefr.knowledge_viewer.PandasTableView import PandasTableView

"""
This class is a child page that displays the results of the constructor.
It displays a table with the results and a button to navigate to the discretizer page.
"""


LOG_DIR: str = '../../logs/'
FILE: str = f'{LOG_DIR}/constructor.tsv'


class ConstructorPage(ChildPage):
    _table_info: QTableView

    # button to navigate to the discretizer page
    _button_discretizer: QPushButton

    def __init__(self, font: QFont, margins: QMargins, button_parent_func: function) -> None:
        super().__init__(font, margins, 'Constructor', button_parent_func)

        # Button to navigate to the discretizer page
        self._button_discretizer = QPushButton('Discretizer', self)
        self._button_discretizer.setFont(font)
        self._layout.insertWidget(1, self._button_discretizer)

        # Load data
        info: DataFrame = pandas.read_csv(FILE, sep='\t')
        # Remove the brackets from the lists
        info.loc[0, 'Blacklist Columns'] = info['Blacklist Columns'][0][1:-1]

        # Create the table and add it to the layout
        self._table_info = PandasTableView(self, info.T, font)
        self._layout.insertWidget(1, self._table_info)

        # Add a spacer to the layout to keep the table at the top
        self._layout.insertItem(2, QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def inject_funcs(self, funcs: list[function]) -> None:
        """
        Inject the functions to be called when the buttons are clicked.
        :param funcs: functions to be injected
        :return: None
        """
        self._button_discretizer.clicked.connect(funcs[0])
