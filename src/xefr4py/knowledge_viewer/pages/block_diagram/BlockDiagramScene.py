import function
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsScene

from xefr4py.knowledge_viewer.pages.block_diagram import ClassBlock


LINE_THICKNESS: int = 3


class BlockDiagramScene(QGraphicsScene):
    """
    This abstract class is used to create a scene for the block diagram.
    Every scene must implement the update_layout and inject_funcs method.
    """
    _line_thickness: int
    _font: QFont

    # List of blocks in the scene
    _blocks: list[ClassBlock]

    def __init__(self, font: QFont, line_thickness: int = LINE_THICKNESS) -> None:
        """
        Constructor of the BlockDiagramScene.

        :param font: font to be used in the blocks
        :param line_thickness: thickness of the lines of the blocks
        """
        super().__init__()
        self._font = font
        self._line_thickness = line_thickness

        # Set the scene's size and position
        self.setSceneRect(0, 0, self.width(), self.height())

    def update_layout(self, width: int, height: int) -> None:
        """
        This method is used to update the layout of the scene.

        :param width: new width of the scene
        :param height: new height of the scene
        :return: None
        """
        # Update the scene's size and position
        self.setSceneRect(0, 0, width, height)

    def inject_funcs(self, functions: list[function]) -> None:
        """
        This method is used to inject the functions into the interactive blocks.
        :param functions: list of functions to be injected
        :return: None
        """
        pass

    def fix_font_size(self) -> None:
        """
        This method is used to fix the font size of the text in the blocks.
        It will make sure that the text fits inside the block and center the text in the block.
        All the blocks will have the same font size.
        """
        biggest_text: ClassBlock = self._blocks[0]

        if biggest_text.rect().width() == 0:
            return

        for block in self._blocks:
            if biggest_text.get_text_item().boundingRect().width() < block.get_text_item().boundingRect().width():
                biggest_text = block

        biggest_text.get_text_item().setFont(self._font)
        font: QFont = self._font

        while biggest_text.get_text_item().boundingRect().width() > biggest_text.rect().width():
            font = QFont(font.family(), font.pointSize() - 1)
            biggest_text.get_text_item().setFont(font)

        for block in self._blocks:
            block.get_text_item().setFont(font)
            block.align_text()
