import function
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont

from xefr4py.knowledge_viewer.pages.block_diagram import BlockDiagramView
from xefr4py.knowledge_viewer.pages.BasePageWithBlockDiagram import BasePageWithBlockDiagram
from xefr4py.knowledge_viewer.pages.ChildPage import ChildPage


class ChildPageWithBlockDiagram(BasePageWithBlockDiagram, ChildPage):
    """
    ChildPageWithBlockDiagram is a base class for pages that have a block diagram
    and a button to navigate to the father page.
    """

    def __init__(self, font: QFont, margins: QMargins, name: str, blockDiagram: BlockDiagramView,
                 father_page: function, **kwargs) -> None:
        """
        Constructor of ChildPageWithBlockDiagram.

        :param font: font of the page
        :param margins: margins of the page
        :param name: name of the page
        :param blockDiagram: block diagram of the page
        :param father_page: function to navigate to the father page
        :param kwargs: additional arguments
        """
        super().__init__(font=font, margins=margins, name=name, blockDiagram=blockDiagram, father_page=father_page)
