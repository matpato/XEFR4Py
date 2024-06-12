from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont

from eefr.knowledge_viewer.Page.BlockDiagram import BlockDiagramView, BlockDiagramScene
from eefr.knowledge_viewer.Page.BlockDiagram.Implementation import MainBlockDiagramScene
from eefr.knowledge_viewer.Page.BasePageWithBlockDiagram import BasePageWithBlockDiagram

"""
This class is the main page of the application.
It displays the main block diagram.
"""


class MainPage(BasePageWithBlockDiagram):

    def __init__(self, font: QFont, margins: QMargins, line_thickness: int) -> None:
        blockDiagram: BlockDiagramScene = MainBlockDiagramScene(font, line_thickness)
        view: BlockDiagramView = BlockDiagramView(blockDiagram)
        super().__init__(font, margins, 'Main', view)


