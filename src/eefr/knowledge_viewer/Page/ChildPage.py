import function
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QPushButton

from eefr.knowledge_viewer.Page.BasePage import BasePage

"""
This class is a child of BasePage. 
It is used to create a page that has a button to navigate to the father page.
"""


ICON_DIRECTORY: str = '../../../resources/icon/'
LEFT_BUTTON_ICON: str = f'{ICON_DIRECTORY}/left-button-icon.webp'


class ChildPage(BasePage):
    _button_father: QPushButton

    def __init__(self, font: QFont, margins: QMargins, name: str, father_page: function, **kwargs) -> None:
        super().__init__(font, margins, name, **kwargs)

        # Button to navigate to the blocks page
        self._button_father = QPushButton('Back', self)
        self._button_father.clicked.connect(lambda: (self.reset(), father_page()))
        self._button_father.setFont(font)
        self._button_father.move(margins.left(), margins.top())
        self._button_father.setIcon(QIcon(LEFT_BUTTON_ICON))
        #self.button_father.setStyleSheet("QPushButton { margin: 0; padding: 0; }")
        #self.layout.addWidget(self.button_father)
