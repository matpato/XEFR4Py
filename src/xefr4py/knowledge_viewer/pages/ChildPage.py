from importlib.abc import Traversable

import function
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QPushButton
from importlib import resources as pkg_resources

from xefr4py.knowledge_viewer.pages.BasePage import BasePage


PACKAGE_NAME: str = 'xefr4py'
ICONS_DIRECTORY: str = 'resources/icons'

ICONS: Traversable = pkg_resources.files(PACKAGE_NAME).joinpath(ICONS_DIRECTORY)

LEFT_BUTTON_ICON: str = str(ICONS.joinpath('left-button-icon.webp'))


class ChildPage(BasePage):
    """
    This class is a child of BasePage.
    It is used to create a page that has a button to navigate to the father page.
    """

    _button_father: QPushButton

    def __init__(self, font: QFont, margins: QMargins, name: str, father_page: function, **kwargs) -> None:
        """
        Constructor of the ChildPage.

        :param font: font of the page
        :param margins: margins of the page
        :param name: name of the page
        :param father_page: function to navigate to the father page
        :param kwargs: optional arguments
        """
        super().__init__(font, margins, name, **kwargs)

        # Button to navigate to the blocks page
        self._button_father = QPushButton('Back', self)
        self._button_father.clicked.connect(lambda: (self.reset(), father_page()))
        self._button_father.setFont(font)
        self._button_father.move(margins.left(), margins.top())
        self._button_father.setIcon(QIcon(LEFT_BUTTON_ICON))
