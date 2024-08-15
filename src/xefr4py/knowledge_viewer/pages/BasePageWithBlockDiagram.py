import function
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont

from xefr4py.knowledge_viewer.pages.block_diagram import BlockDiagramView
from xefr4py.knowledge_viewer.pages.BasePage import BasePage


class BasePageWithBlockDiagram(BasePage):
    """
    BasePageWithBlockDiagram is a base class for pages that have a block diagram.
    It is a subclass of BasePage and has a block diagram as an attribute.
    """
    _blockDiagram: BlockDiagramView

    def __init__(self, font: QFont, margins: QMargins, name: str, blockDiagram: BlockDiagramView, **kwargs) -> None:
        """
        Constructor for BasePageWithBlockDiagram.

        :param font: font to be used in the page
        :param margins: margins to be used in the page
        :param name: name of the page
        :param blockDiagram: block diagram to be used in the page
        :param kwargs: additional arguments
        """
        super().__init__(font, margins, name, **kwargs)
        self._blockDiagram = blockDiagram
        self._layout.addWidget(self._blockDiagram)

    def inject_funcs(self, functions: list[function]) -> None:
        """
        Inject functions into block diagram

        :param functions: functions to be injected
        """
        # Inject functions into block diagram
        self._blockDiagram.inject_funcs(functions)
