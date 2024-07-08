from typing import overload

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem


# Default colors
BRUSH_COLOR = Qt.white
PEN_COLOR = Qt.black


class ClassBlock(QGraphicsRectItem):
    """
    This class is a QGraphicsRectItem that represents a class block in the diagram.
    It has a text item that represents the class name.
    The text item is centered in the rectangle.
    """
    _text_item: QGraphicsTextItem
    _font: QFont

    _line_thickness: int

    def __init__(self, x: int, y: int, width: int, height: int, line_thickness: int, text: str = None,
                 font: QFont = None) -> None:
        """
        Constructor of the ClassBlock.

        :param x: x position of the block
        :param y: y position of the block
        :param width: width of the block
        :param height: height of the block
        :param line_thickness: thickness of the lines of the block
        :param text: text of the block
        :param font: font of the text
        """
        super().__init__(x, y, width, height)

        self._line_thickness = line_thickness
        self._font = font

        # Set the default colors
        self.setPen(QPen(PEN_COLOR, line_thickness))
        self.setBrush(BRUSH_COLOR)

        # Create a text item
        self._text_item = QGraphicsTextItem(text, self)
        self._text_item.setDefaultTextColor(Qt.black)
        self._text_item.setParentItem(self)
        if font is not None:
            self._text_item.setFont(font)

        # Set the text position to the center of the rectangle
        self.align_text()

    @overload
    def setRect(self, rect: QRectF) -> None:
        """
        Overload of the setRect method to accept a QRectF object

        :param rect: QRectF that represents the new rectangle
        """
        pass

    # noinspection PyMethodOverriding
    @overload
    def setRect(self, x: float, y: float, width: float, height: float) -> None:
        """
        Overload of the setRect method to accept the x, y, width and height of the new rectangle

        :param x: x coordinate of the new rectangle
        :param y: y coordinate of the new rectangle
        :param width: width of the new rectangle
        :param height: height of the new rectangle
        """
        pass

    def setRect(self, *args) -> None:
        """
        Base method to set the rectangle of the class block

        :param args: parameters expressed in the overloads
        """
        super().setRect(*args)

    def align_text(self) -> None:
        """
        Aligns the text item to the center of the rectangle
        """
        # Get the width and height of the text item
        text_width = self._text_item.boundingRect().width()
        text_height = self._text_item.boundingRect().height()

        # Calculate the position of the text item
        text_x = self.rect().center().x() - text_width / 2
        text_y = self.rect().center().y() - text_height / 2
        self._text_item.setPos(text_x, text_y)

    def get_text_item(self) -> QGraphicsTextItem:
        """
        Returns the text item of the class block

        :return: QGraphicsTextItem text item
        """
        return self._text_item
