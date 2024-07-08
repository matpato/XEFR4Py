from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableView, QTableWidget, QWidget
from pandas import DataFrame

from eefr.knowledge_viewer.pages.table.PandasModel import PandasModel


class PandasTableView(QTableView):
    """
    PanadasTableView is a class that extends QTableView and is used to display a pandas DataFrame in a table.
    It uses the PandasModel to display the data and has the aspect that we pretend to use in the Knowledge Viewer App.
    """

    def __init__(self, parent: QWidget | None, info: DataFrame, font: QFont):
        """
        Constructor of the PandasTableView.

        :param parent: parent of the table
        :param info: DataFrame to be displayed
        :param font: font to be used in the table
        """
        super().__init__(parent)

        # Define the Pandas model
        self.setModel(PandasModel(info))

        # Resize the table, hide the headers and set the font
        self.horizontalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)
        self.setFixedHeight(sum([self.rowHeight(i) for i in range(info.shape[0])]) + 2)     # 2 is the border width
        self.horizontalScrollMode()
        self.verticalScrollMode()
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setFont(font)
