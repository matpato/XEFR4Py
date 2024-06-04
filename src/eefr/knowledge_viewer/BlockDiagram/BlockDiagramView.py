from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QResizeEvent
from PyQt5.QtWidgets import QGraphicsView

from eefr.knowledge_viewer.BlockDiagram import BlockDiagramScene

"""
This class is used to create a view for the block diagram.
The constructor takes a scene that implements the interface BlockDiagramScene.
The view is automatically updated when it is resized.
"""


class BlockDiagramView(QGraphicsView):
    # blocks diagram
    _scene: BlockDiagramScene

    def __init__(self, scene: BlockDiagramScene) -> None:
        super().__init__()

        # Set border to none in the style sheet
        self.setStyleSheet("border: none;")

        # Set up the scene
        self._scene = scene
        self.setScene(self._scene)

        # Set the view parameters
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        This method is called when the view is resized.
        :param event: QResizeEvent that was the info for the resize
        :return: None
        """
        # Call the updateLayout method on the scene when the view is resized
        self._scene.update_layout(event.size().width(), event.size().height())

    def inject_funcs(self, functions) -> None:
        """
        This method is used to inject the functions into the interactive blocks.
        It is used to abstract the user from the underlying BlockDiagramScene.
        :param functions: list of functions to be injected
        :return: None
        """
        self._scene.inject_funcs(functions)
