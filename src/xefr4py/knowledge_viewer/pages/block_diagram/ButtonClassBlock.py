import function
from PyQt5.QtGui import QColor, QFont, QPen
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent

from xefr4py.knowledge_viewer.pages.block_diagram.ClassBlock import ClassBlock, PEN_COLOR, BRUSH_COLOR


# Colors of the button when the mouse is over it
# Same colors of the default button
HOVER_PEN_COLOR = QColor(21, 130, 214, 255)
HOVER_BRUSH_COLOR = QColor(224, 238, 249, 255)


class ButtonClassBlock(ClassBlock):
    """
    ClassBlock with a function that is called when the button is clicked.
    It extends the ClassBlock and also changes the color when the mouse is over the button.
    """
    _func: function

    def __init__(self, x: int, y: int, width: int, height: int, line_thickness: int, text: str = None,
                 font: QFont = None) -> None:
        """
        Constructor of the ButtonClassBlock.

        :param x: x position of the block
        :param y: y position of the block
        :param width: width of the block
        :param height: height of the block
        """
        super().__init__(x, y, width, height, line_thickness, text, font)
        # enable hover events
        self.setAcceptHoverEvents(True)

    def inject_func(self, func: function) -> None:
        """
        Inject the function that will be called when the button is clicked.

        :param func: function to be called
        """
        self._func = func

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Call the function when the button is clicked.

        :param event: event that triggered the function
        :return: None
        """
        self._func()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """
        Change the color of the button to the hover when the mouse is over it.

        :param event: event that triggered the function
        :return: None
        """
        self.setPen(QPen(HOVER_PEN_COLOR, self._line_thickness))
        self.setBrush(QColor(HOVER_BRUSH_COLOR))

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """
        Change the color of the button to the default when the mouse is not over it.

        :param event: event that triggered the function
        :return: None
        """
        self.setPen(QPen(PEN_COLOR, self._line_thickness))
        self.setBrush(QColor(BRUSH_COLOR))
