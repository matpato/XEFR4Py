from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsLineItem

from eefr.knowledge_viewer.pages.block_diagram.ClassBlock import ClassBlock

LINE_THICKNESS: int = 3

"""
This class is used to draw an arrow between two class blocks.
"""


def get_line_pos(start_block: ClassBlock, end_block: ClassBlock) -> (int, int, int, int):
    """
    This function calculates the start and end points of the line between two class blocks.
    :param start_block: start class block
    :param end_block: end class block
    :return: points of the line
    """
    # get the center of the blocks
    start_block_x: int = int(start_block.rect().center().x())
    start_block_y: int = int(start_block.rect().center().y())

    end_block_x: int = int(end_block.rect().center().x())
    end_block_y: int = int(end_block.rect().center().y())

    # calculate the difference between the start and end blocks
    dx: int = end_block_x - start_block_x
    dy: int = end_block_y - start_block_y

    start_line_x: int
    start_line_y: int

    end_line_x: int
    end_line_y: int

    # calculate the start and end points of the line
    if dy == 0:
        if dx > 0:  # right
            start_line_x = int(start_block_x + start_block.rect().width() / 2)
            end_line_x = int(end_block_x - end_block.rect().width() / 2)
        else:       # left
            start_line_x = int(start_block_x - start_block.rect().width() / 2)
            end_line_x = int(end_block_x + end_block.rect().width() / 2)
        start_line_y = start_block_y
        end_line_y = end_block_y
    else:
        if dy > 0:  # down
            start_line_y = int(start_block_y + start_block.rect().height() / 2)
            end_line_y = int(end_block_y - end_block.rect().height() / 2)
        else:       # up
            start_line_y = int(start_block_y - start_block.rect().height() / 2)
            end_line_y = int(end_block_y + end_block.rect().height() / 2)
        start_line_x = start_block_x
        end_line_x = end_block_x

    return end_line_x, end_line_y, start_line_x, start_line_y


def get_tip_points(start_x: int, start_y: int, end_x: int, end_y: int, line_thickness) -> QPolygonF:
    """
    This function calculates the points of the arrowhead.
    :param start_x: x coordinate of the start point
    :param start_y: y coordinate of the start point
    :param end_x: x coordinate of the end point
    :param end_y: y coordinate of the end point
    :param line_thickness: thickness of the line
    :return: arrow head
    """
    # calculate the difference between the start and end points
    dx: int = end_x - start_x
    dy: int = end_y - start_y

    # calculate the size of the arrowhead
    tip_size: int = line_thickness * 4
    half: int = tip_size // 2

    tip: QPolygonF

    # Point arrowhead in the right direction
    if dy == 0:
        if dx > 0:  # right
            tip = QPolygonF([QPoint(end_x - tip_size, end_y - half), QPoint(end_x - tip_size, end_y + half),
                             QPoint(end_x, end_y)])
        else:       # left
            tip = QPolygonF([QPoint(end_x + tip_size, end_y - half), QPoint(end_x + tip_size, end_y + half),
                             QPoint(end_x, end_y)])
    else:
        if dy > 0:  # down
            tip = QPolygonF([QPoint(end_x - half, end_y + tip_size), QPoint(end_x + half, end_y + tip_size),
                             QPoint(end_x, end_y)])
        else:       # up
            tip = QPolygonF([QPoint(end_x - half, end_y - tip_size), QPoint(end_x + half, end_y - tip_size),
                             QPoint(end_x, end_y)])

    return tip


class Arrow(QGraphicsLineItem):
    # This class is used to draw an arrow between two class blocks.
    tip: QGraphicsPolygonItem
    line_thickness: int

    def __init__(self, start_block: ClassBlock, end_block: ClassBlock, line_thickness: int = LINE_THICKNESS):
        # calculate the start and end points of the line
        pos: (int, int, int, int) = get_line_pos(end_block, start_block)
        # draw the line
        super().__init__(*pos)
        self.line_thickness = line_thickness
        self.setPen(QPen(Qt.black, line_thickness))

        # draw the arrowhead
        self.tip = QGraphicsPolygonItem(get_tip_points(*pos, line_thickness))
        self.tip.setPen(QPen(Qt.black, line_thickness))
        self.tip.setParentItem(self)
        self.tip.setBrush(Qt.black)

    def updateArrow(self, start_block: ClassBlock, end_block: ClassBlock) -> None:
        """
        This function updates the arrow between two class blocks.
        :param start_block: start class block
        :param end_block: end class block
        :return: None
        """
        pos: (int, int, int, int) = get_line_pos(end_block, start_block)
        self.tip.setPolygon(get_tip_points(*pos, self.line_thickness))
        self.setLine(*pos)
