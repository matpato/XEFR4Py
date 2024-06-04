import function
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont

from eefr.knowledge_viewer.BlockDiagram import BlockDiagramView
from eefr.knowledge_viewer.Page.BasePage import BasePage

"""
BasePageWithBlockDiagram is a base class for pages that have a block diagram.
It is a subclass of BasePage and has a block diagram as an attribute.
"""


class BasePageWithBlockDiagram(BasePage):
    _blockDiagram: BlockDiagramView

    def __init__(self, font: QFont, margins: QMargins, name: str, blockDiagram: BlockDiagramView, **kwargs) -> None:
        super().__init__(font, margins, name, **kwargs)
        self._blockDiagram = blockDiagram
        self._layout.addWidget(self._blockDiagram)

    def inject_funcs(self, functions: list[function]) -> None:
        """
        Inject functions into block diagram
        :param functions: functions to be injected
        :return: None
        """
        # Inject functions into block diagram
        self._blockDiagram.inject_funcs(functions)
