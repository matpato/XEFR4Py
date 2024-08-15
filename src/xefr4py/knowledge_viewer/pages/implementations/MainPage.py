from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont

from xefr4py.knowledge_viewer.pages.block_diagram import BlockDiagramView, BlockDiagramScene
from xefr4py.knowledge_viewer.pages.block_diagram.implementations import MainBlockDiagramScene
from xefr4py.knowledge_viewer.pages.BasePageWithBlockDiagram import BasePageWithBlockDiagram

"""
This class is the main page of the application.
It displays the main block diagram.
"""


class MainPage(BasePageWithBlockDiagram):

    def __init__(self, font: QFont, margins: QMargins, line_thickness: int) -> None:
        blockDiagram: BlockDiagramScene = MainBlockDiagramScene(font, line_thickness)
        view: BlockDiagramView = BlockDiagramView(blockDiagram)
        super().__init__(font, margins, 'Main', view)


