# this code is from https://github.com/eyllanesc/stackoverflow/blob/master/questions/44603119/PandasModel.py
from typing import Any

import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt


class PandasModel(QtCore.QAbstractTableModel):
    """
    Pandas Model is an implementation of QAbstractTableModel for use with Pandas DataFrames.
    """

    def __init__(self, df=pd.DataFrame(), parent=None) -> None:
        """
        Constructor of the PandasModel

        :param df: DataFrame to be used
        :param parent: parent of the model
        """
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        """
        Get the header data for the model

        :param section: number of the section
        :param orientation: orientation of the header
        :param role: int role
        :return: data of the header
        """
        if role != Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index: QModelIndex, role=Qt.DisplayRole) -> Any:
        """
        Get the data for the model

        :param index: index of the data
        :param role: role of the data
        :return: data of the index
        """
        if role != Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.DisplayRole) -> bool:
        """
        Set the data for the model

        :param index: index of the data
        :param value: value to set
        :param role: role of the data
        :return: if it was set
        """
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Get the row count of the model

        :param parent: parent index
        :return: row count
        """
        return len(self._df.index)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Get the column count of the model

        :param parent: parent index
        :return: column count
        """
        return len(self._df.columns)

    def sort(self, column: int, order: Qt.SortOrder = Qt.DescendingOrder) -> None:
        """
        Sort the column by the passed order

        :param column: number of the column to sort
        :param order: order to sort
        :return: None
        """
        col_name = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(col_name, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
