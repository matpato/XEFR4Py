import function
from PyQt5.QtGui import QFont

from eefr.knowledge_viewer.BlockDiagram import ButtonClassBlock, Arrow, BlockDiagramScene
from eefr.knowledge_viewer.BlockDiagram.BlockDiagramScene import LINE_THICKNESS


"""
Class for the ensemble feature ranking block diagram.
This class is a subclass of the BlockDiagramScene class.
It contains the block diagram for the ensemble feature ranking.
"""
HORIZONTAL_CELLS: int = 5
VERTICAL_CELLS: int = 3


class EnsembleFeatureRankingBlockDiagramScene(BlockDiagramScene):
    # Blocks
    _subsets: ButtonClassBlock
    _weights: ButtonClassBlock
    _rank: ButtonClassBlock

    # Arrows
    _arrow1: Arrow
    _arrow2: Arrow

    def __init__(self, font: QFont, line_thickness: int = LINE_THICKNESS):
        super().__init__(font, line_thickness)

        # Get the width and height of the scene
        width: int = int(self.width())
        height: int = int(self.height())

        # Calculate the block width and height
        block_width: int = int(width / HORIZONTAL_CELLS)
        block_height: int = int(height / VERTICAL_CELLS)

        # Create interactive blocks
        self._subsets = ButtonClassBlock(0, block_height, block_width, block_height, line_thickness,
                                         "get N Random Rows Subsets", font)
        self._weights = ButtonClassBlock(block_width * 2, block_height, block_width, block_height, line_thickness,
                                         "calculate Weights Sampling", font)
        self._rank = ButtonClassBlock(block_width * 4, block_height, block_width, block_height, line_thickness,
                                      "calculate Rank Sampling", font)

        # Create arrows to connect the blocks
        self._arrow1 = Arrow(self._subsets, self._weights, line_thickness)
        self._arrow2 = Arrow(self._weights, self._rank, line_thickness)

        # Add blocks, line, and arrowhead to the scene
        self.addItem(self._subsets)
        self.addItem(self._weights)
        self.addItem(self._rank)
        self.addItem(self._arrow1)
        self.addItem(self._arrow2)

        self._blocks = [self._subsets, self._weights, self._rank]

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
        self._subsets.setRect(0, block_height, block_width, block_height)
        self._weights.setRect(block_width * 2, block_height, block_width, block_height)
        self._rank.setRect(block_width * 4, block_height, block_width, block_height)
        self._arrow1.updateArrow(self._subsets, self._weights)
        self._arrow2.updateArrow(self._weights, self._rank)

        # Update the font size of the blocks to make sure the text fits
        self.fix_font_size()

    def inject_funcs(self, functions: list[function]) -> None:
        """
        Inject the functions into the clickable blocks.
        :param functions: the functions to be injected
        :return: None
        """
        self._subsets.inject_func(functions[0])
        self._weights.inject_func(functions[1])
        self._rank.inject_func(functions[2])
