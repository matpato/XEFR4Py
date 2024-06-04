from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableView, QTableWidget, QWidget
from pandas import DataFrame

from eefr.knowledge_viewer.PandasModel import PandasModel

"""
PanadasTableView is a class that extends QTableView and is used to display a pandas DataFrame in a table.
It uses the PandasModel to display the data and has the aspect that we pretend to use in the Knowledge Viewer App.
"""


class PandasTableView(QTableView):
    def __init__(self, parent: QWidget | None, info: DataFrame, font: QFont):
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

        # increase the visibility of the table, by making the recognition of the rows easier
        # self.setAlternatingRowColors(True)
        # don't show the borderline, but it removes the formation of the index
        # self.setStyleSheet("QTableView {border: none;}")
