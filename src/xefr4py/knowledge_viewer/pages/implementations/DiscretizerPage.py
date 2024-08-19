import function
import mplcursors
import pandas
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from pandas import DataFrame

from xefr4py.Utils import get_log_dir
from xefr4py.knowledge_viewer.pages.ChildPage import ChildPage
from xefr4py.knowledge_viewer.pages.table.PandasTableView import PandasTableView

"""
This class is a child page that displays the results of the discretizer.
It displays a table with the results and a histogram with the classes distribution.
"""

LOG_DIR: str = get_log_dir()

class DiscretizerPage(ChildPage):
    _table_info: PandasTableView

    def __init__(self, font: QFont, margins: QMargins, father_page: function):
        super().__init__(font, margins, 'Discretizer', father_page)

        # Load data
        info: DataFrame = pandas.read_csv(f'{LOG_DIR}/discretizer.tsv', sep='\t')

        # Get classes and counts
        classes: list[str] = info['Classes'][0][1:-1].split()
        counts: list[int] = [int(s) for s in info['Classes Distribution'][0][1:-1].split()]

        # Plot histogram
        plt.figure()  # Adjust figure size as needed
        plt.bar(classes, counts)

        # Add hover to show details
        mplcursors.cursor(plt.gcf(), hover=2)

        # Customize plot
        plt.xlabel('Classes')
        plt.ylabel('Counts')
        plt.title("Histogram of Discretized Classes")
        plt.tight_layout()

        # Add plot to layout
        self._layout.insertWidget(1, FigureCanvasQTAgg(plt.gcf()), stretch=1)

        # Remove unnecessary columns
        info = info.drop(['Classes', 'Classes Distribution'], axis=1)

        # Add table to layout
        self._table_info = PandasTableView(self, info.T, font)
        self._layout.insertWidget(1, self._table_info, stretch=0)
