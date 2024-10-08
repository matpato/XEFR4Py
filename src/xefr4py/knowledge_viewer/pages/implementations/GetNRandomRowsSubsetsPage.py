import function
import pandas
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from pandas import DataFrame

from xefr4py.Utils import get_log_dir
from xefr4py.knowledge_viewer.pages.ChildPage import ChildPage
from xefr4py.knowledge_viewer.pages.table import PandasTableView

"""
This class is a child page that displays the results of the get n random subsets.
It shows a table with the results.
"""


LOG_DIR: str = get_log_dir()
FILE: str = f'{LOG_DIR}/get_n_randoms_rows_subsets.tsv'


class GetNRandomRowsSubsetsPage(ChildPage):
    _table_info: PandasTableView

    def __init__(self, font: QFont, margins: QMargins, button_parent_func: function):
        super().__init__(font, margins, 'Get N Random Rows Subsets', button_parent_func)

        # Load the data
        info: DataFrame = pandas.read_csv(FILE, sep='\t')

        # Create the table and add it to the layout
        self._table_info = PandasTableView(self, info.T, font)
        self._layout.insertWidget(1, self._table_info)

        # Add a spacer to the layout to keep things in place
        self._layout.insertItem(2, QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
