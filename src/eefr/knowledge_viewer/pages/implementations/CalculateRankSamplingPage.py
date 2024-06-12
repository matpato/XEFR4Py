import function
import mplcursors
import pandas
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableView, QSpinBox, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from pandas import DataFrame

from eefr.knowledge_viewer.pages.ChildPage import ChildPage
from eefr.knowledge_viewer.pages.table.PandasTableView import PandasTableView

"""
This class is a child page that displays the results of the rank sampling calculation.
It displays a table with the results and a diagram with the top features.
Its possible to select the number of columns to display in the diagram.
"""

# File paths to get the data to display
LOG_DIR: str = '../../logs/'
FILE: str = f'{LOG_DIR}/calculate_rank_sampling.tsv'
GRAPH_FILE: str = F'{LOG_DIR}/rank_sampling.tsv'

# Default and max number of columns to display in the diagrams
MAX_COLS: int = 100
COLS: int = 10

# Color for the bars in the diagram
BAR_COLOR: str = 'tab:blue'


class CalculateRankSamplingPage(ChildPage):
    _diagram: FigureCanvasQTAgg
    _diagram_info: DataFrame
    _table_info: QTableView

    def __init__(self, font: QFont, margins: QMargins, button_parent_func: function) -> None:
        super().__init__(font, margins, 'Calculate Rank Sampling', button_parent_func)

        # Load data
        info: DataFrame = pandas.read_csv(FILE, sep='\t')
        self._diagram_info = pandas.read_csv(GRAPH_FILE, sep='\t')

        # Create table and add it to layout
        self._table_info = PandasTableView(self, info.T, font)
        self._layout.insertWidget(1, self._table_info)

        # Create a layout to select the number of columns
        col_selection_layout: QHBoxLayout = QHBoxLayout(self)

        # Create the label and set the font
        label: QLabel = QLabel("Number of Columns:")
        label.setFont(font)

        # Create the spin box to select the number of columns, configure it and set the font
        self.num_col_box = QSpinBox(self)
        self.num_col_box.setRange(1, min(self._diagram_info.shape[1], MAX_COLS))
        self.num_col_box.setValue(COLS)
        self.num_col_box.valueChanged.connect(self.update_diagram)
        self.num_col_box.setFont(font)

        # Add the label and the spin box to the layout
        col_selection_layout.addWidget(label)
        col_selection_layout.addWidget(self.num_col_box)
        col_selection_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Add the layout to the main layout
        self._layout.insertLayout(2, col_selection_layout)

        # Create the diagram and add it to the layout
        self._diagram = self.generate_diagram(COLS)
        self._layout.insertWidget(3, self._diagram, stretch=1)

    def generate_diagram(self, num_cols: int) -> FigureCanvasQTAgg:
        """
        Generate a diagram with the top features.
        :param num_cols: number of columns to display
        :return: FigureCanvasQTAgg with the diagram
        """
        # Get the data to plot
        classes: list[str] = self._diagram_info.columns[:num_cols].tolist()
        counts: list[float] = self._diagram_info.iloc[0, :num_cols].tolist()

        # Plot the histogram
        plt.figure()  # Adjust figure size as needed
        plt.bar(classes, counts, color=BAR_COLOR)

        # Add hover to show details
        mplcursors.cursor(plt.gcf(), hover=2)

        # Customize plot
        plt.xlabel('Features')
        plt.ylabel('Counts')
        plt.title("Features Rank")
        plt.yscale('log')
        # remove column labels if there are too many columns
        if num_cols > 50:
            plt.xticks([])
        else:
            plt.xticks(rotation=45)
        plt.tight_layout()

        return FigureCanvasQTAgg(plt.gcf())

    def update_diagram(self, num_cols: int) -> None:
        """
        Update the diagram with the new number of columns.
        :param num_cols: number of columns to display
        :return: None
        """
        # Clear the existing diagram
        self._layout.removeWidget(self._diagram)
        self._diagram.close()
        plt.close()

        # Generate the diagram
        self._diagram = self.generate_diagram(num_cols)

        # Update the canvas widget with the new diagram
        self._layout.insertWidget(3, self._diagram, stretch=1)

    def reset(self) -> None:
        """
        Reset the page to its initial state.
        :return: None
        """
        self.num_col_box.setValue(COLS)
