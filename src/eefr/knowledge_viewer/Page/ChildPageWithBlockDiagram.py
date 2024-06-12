import function
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont

from eefr.knowledge_viewer.Page.BlockDiagram import BlockDiagramView
from eefr.knowledge_viewer.Page.BasePageWithBlockDiagram import BasePageWithBlockDiagram
from eefr.knowledge_viewer.Page.ChildPage import ChildPage

"""
ChildPageWithBlockDiagram is a base class for pages that have a block diagram 
and a button to navigate to the father page.
"""


class ChildPageWithBlockDiagram(BasePageWithBlockDiagram, ChildPage):

    def __init__(self, font: QFont, margins: QMargins, name: str, blockDiagram: BlockDiagramView,
                 father_page: function, **kwargs) -> None:
        super().__init__(font=font, margins=margins, name=name, blockDiagram=blockDiagram, father_page=father_page)
