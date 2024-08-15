import function
from PyQt5.QtGui import QFont

from xefr4py.knowledge_viewer.pages.block_diagram import ButtonClassBlock, Arrow, BlockDiagramScene
from xefr4py.knowledge_viewer.pages.block_diagram.BlockDiagramScene import LINE_THICKNESS


HORIZONTAL_CELLS: int = 3
VERTICAL_CELLS: int = 3


class MainBlockDiagramScene(BlockDiagramScene):
    """
    Class for the main block diagram.
    This class is a subclass of BlockDiagramScene.
    It contains the main block diagram.
    """

    # Blocks
    _init: ButtonClassBlock
    _efr: ButtonClassBlock

    # Arrow
    _arrow: Arrow

    def __init__(self, font: QFont, line_thickness: int = LINE_THICKNESS):
        super().__init__(font, line_thickness)

        # Get the width and height of the scene
        width: int = int(self.width())
        height: int = int(self.height())

        # Calculate the width and height of the blocks
        block_width: int = int(width / 3)
        block_height: int = int(height / 3)

        # Create interactive blocks
        self._init = ButtonClassBlock(0, block_height, block_width, block_height, line_thickness,
                                      "Constructor", font)
        self._efr = ButtonClassBlock(block_width * 2, block_height, block_width, block_height, line_thickness,
                                     "Ensemble Feature Rank", font)

        # Create arrows to connect the blocks
        self._arrow = Arrow(self._init, self._efr, line_thickness)

        # Add blocks, line, and arrowhead to the scene
        self.addItem(self._init)
        self.addItem(self._efr)
        self.addItem(self._arrow)

        self._blocks = [self._init, self._efr]

    def update_layout(self, width: int, height: int) -> None:
        """
        Update the layout of the scene. This method is called when the window is resized.
        It updates the position and size of the blocks and arrows.

        :param width: the new width of the scene
        :param height: the new height of the scene
        :return: None
        """
        # Update the layout of the superclass
        super().update_layout(width, height)

        # calculate the new block width and height
        block_width: int = int(width / HORIZONTAL_CELLS)
        block_height: int = int(height / VERTICAL_CELLS)

        # Update the layout based on the new width and height
        self._init.setRect(0, block_height, block_width, block_height)
        self._efr.setRect(block_width * 2, block_height, block_width, block_height)
        self._arrow.updateArrow(self._init, self._efr)

        # Update the font size of the blocks to make sure the text fits
        self.fix_font_size()

    def inject_funcs(self, functions: list[function]) -> None:
        """
        Inject the functions into the clickable blocks.

        :param functions: the functions to be injected
        :return: None
        """
        self._init.inject_func(functions[0])
        self._efr.inject_func(functions[1])
