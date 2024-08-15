from PyQt5.QtCore import QMargins, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class BasePage(QWidget):
    """
    BasePage is a class that is used to create a base page for the application.
    It only contains a vertical layout and a text label.
    """

    _layout: QVBoxLayout
    _label: QLabel

    def __init__(self, font: QFont, margins: QMargins, name: str, **kwargs) -> None:
        """
        Constructor for the BasePage class.

        :param font: font for the label
        :param margins: margins for the layout
        :param name: name of the page
        :param kwargs: additional arguments
        """
        super().__init__(**kwargs)

        # Create a vertical layout for the page
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(margins)

        # Label to display the content of the page
        self._label = QLabel(name, self)
        self._label.setFont(font)
        self._label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self._label)

    def reset(self) -> None:
        """
        Reset the page to its initial state
        """
        return
