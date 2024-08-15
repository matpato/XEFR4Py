import function
import mplcursors
import pandas
import importlib.resources as pkg_resources
from PyQt5.QtCore import QMargins, Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSplitter, QPushButton, QLabel, QSpinBox, QHBoxLayout, QSpacerItem, QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from pandas import DataFrame

from Utils import get_log_dir
from xefr4py.knowledge_viewer.pages.ChildPage import ChildPage
from xefr4py.knowledge_viewer.pages.table.PandasTableView import PandasTableView

"""
This class is a child page that displays the results of the metric.
It displays a table with the results and a diagram with the top features for the metric.
"""

COLS: int = 10
MAX_COLS: int = 100
NOT_SELECTECTED: str = ''

SELECTED_COLOR: str = 'green'
BAR_COLOR: str = 'tab:blue'

FRAME_TIME: int = 1000  # milliseconds

LOGS_DIRECTORY: str = get_log_dir()

ICON_DIRECTORY: str = "resources.icons"
PLAY_BUTTON_ICON: str = str(pkg_resources.path(ICON_DIRECTORY, 'play-button-icon.webp'))
PAUSE_BUTTON_ICON: str = str(pkg_resources.path(ICON_DIRECTORY, 'pause-button-icon.webp'))
STOP_BUTTON_ICON: str = str(pkg_resources.path(ICON_DIRECTORY, 'stop-button-icon-2.webp'))
LEFT_BUTTON_ICON: str = str(pkg_resources.path(ICON_DIRECTORY, 'left-button-icon.webp'))
RIGHT_BUTTON_ICON: str = str(pkg_resources.path(ICON_DIRECTORY, 'right-button-icon.webp'))


class MetricPage(ChildPage):
    _table_info: PandasTableView
    _diagrams: QSplitter

    # buttons to navigate through the diagrams of the iterations
    _button_previous: QPushButton
    _button_next: QPushButton

    # buttons to control the animation
    _pause_button: QPushButton
    _stop_button: QPushButton

    # QTimer to control the animation and the diagram
    _selected_column: str = NOT_SELECTECTED
    _animation_running: bool = False
    _animation_delay = FRAME_TIME
    _num_col_box: QSpinBox

    _weights: DataFrame
    _index: int = 0
    _name: str

    def __init__(self, font: QFont, margins: QMargins, name: str, father_page: function) -> None:
        super().__init__(font, margins, name, father_page)

        self._name = name
        name = name.replace(' ', '_')

        # Load the data
        info: DataFrame = pandas.read_csv(f'{LOGS_DIRECTORY}/{name}.tsv', sep='\t')
        self._weights = pandas.read_csv(f'{LOGS_DIRECTORY}/metric_{name}.tsv', sep='\t')

        self._table_info = PandasTableView(self, info.T, font)
        self._layout.insertWidget(1, self._table_info, stretch=0)

        # Create the label and set the font
        label: QLabel = QLabel("Number of Columns:")
        label.setFont(font)

        # Create the spin box to select the number of columns, configure it and set the font
        self._num_col_box = QSpinBox(self)
        self._num_col_box.setRange(1, min(self._weights.shape[1], MAX_COLS))
        self._num_col_box.setValue(COLS)
        self._num_col_box.valueChanged.connect(self.update_diagrams)
        self._num_col_box.setFont(font)

        # Create a layout for the buttons to navigate through the diagrams
        ll: QHBoxLayout = QHBoxLayout(self)
        lr: QHBoxLayout = QHBoxLayout(self)

        # Add the label and the spin box to the layout
        ll.addWidget(label)
        ll.addWidget(self._num_col_box)
        ll.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        l: QHBoxLayout = QHBoxLayout(self)
        l.addLayout(ll)
        l.addLayout(lr)
        self._layout.insertLayout(2, l)

        # Add the buttons to navigate through the diagrams
        if self._weights.shape[0] > 1:
            # Add the buttons to navigate through the diagrams
            self._button_previous = QPushButton('Previous', self)
            self._button_previous.clicked.connect(self.button_previous_func)
            self._button_previous.setFont(font)
            self._button_previous.setIcon(QIcon(LEFT_BUTTON_ICON))
            ll.addWidget(self._button_previous)

            self._button_next = QPushButton('   Next   ', self)
            self._button_next.clicked.connect(self.button_next_func)
            self._button_next.setFont(font)
            self._button_next.setIcon(QIcon(RIGHT_BUTTON_ICON))
            self._button_next.setLayoutDirection(Qt.RightToLeft)
            lr.addWidget(self._button_next)

            # Create the play/pause button to control the animation
            self._pause_button = QPushButton(self)
            self._pause_button.setIcon(QIcon(PLAY_BUTTON_ICON))
            self._pause_button.clicked.connect(self.toggle_animation)

            # Create the stop button to stop the animation
            self._stop_button = QPushButton(self)
            self._stop_button.setIcon(QIcon(STOP_BUTTON_ICON))
            self._stop_button.clicked.connect(self.stop_animation)

            # Add the animation buttons to the layout
            lr.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
            lr.addWidget(self._pause_button)
            lr.addWidget(self._stop_button)

            # Initialize QTimer for animation
            self.animation_timer = QTimer(self)
            self.animation_timer.timeout.connect(self.button_next_func)

        # Create a layout to display the diagrams
        self._diagrams = QSplitter(Qt.Horizontal, self)

        # Generate the diagrams
        self.generate_diagrams(COLS)
        self._layout.insertWidget(3, self._diagrams, stretch=1)

    def toggle_animation(self) -> None:
        """
        Toggle the animation (start or pause it)
        We consider the animation the iteration through the diagrams
        :return: None
        """
        if self._animation_running:
            self.pause_animation()
        else:
            self.start_animation()

    def start_animation(self) -> None:
        """
        Start the animation (iteration through the diagrams)
        :return: None
        """
        self.animation_timer.start(self._animation_delay)
        self._animation_running = True
        self._pause_button.setIcon(QIcon(PAUSE_BUTTON_ICON))

    def pause_animation(self) -> None:
        """
        Pause the animation (iteration through the diagrams)
        Can be resumed by calling start_animation
        :return: None
        """
        self.animation_timer.stop()
        self._animation_running = False
        self._pause_button.setIcon(QIcon(PLAY_BUTTON_ICON))

    def stop_animation(self) -> None:
        """
        Stop the animation (iteration through the diagrams)
        It resets the index to 0, stops the QTimer and removes the selected column
        :return:
        """
        self.animation_timer.stop()
        self._animation_running = False
        self._pause_button.setIcon(QIcon(PLAY_BUTTON_ICON))
        self._index = 0
        self._selected_column = NOT_SELECTECTED
        self.update_diagrams()

    def button_previous_func(self) -> None:
        """
        Move to the previous diagram
        :return: None
        """
        self._index = (self._index - 1) % self._weights.shape[0]
        self.update_diagrams()

    def button_next_func(self) -> None:
        """
        Move to the next diagram
        If the index is the last one, it pauses the animation
        :return: None
        """
        self._index = (self._index + 1) % self._weights.shape[0]
        if self._index == self._weights.shape[0] - 1:
            self.pause_animation()
        self.update_diagrams()

    def generate_diagrams(self, num_cols: int) -> None:
        """
        Generate the diagrams for the selected metric
        :param num_cols: number of columns to display
        :return: None
        """
        # Get the rows and sort it
        d: DataFrame = DataFrame(self._weights.loc[:self._index])
        d = d.sum(axis=0).sort_values(ascending=False)[:][:num_cols]

        # Extract column names and corresponding values
        columns = d.index.tolist()
        values = d.tolist()

        # Add the cumulative metric diagram
        self._diagrams.addWidget(self.generate_diagram(
            columns, values, f'Cumulative {self._name} {self._index}', self._weights.shape[0]))

        # Get the row and sort it
        d: DataFrame = DataFrame(self._weights.loc[self._index])
        d = d.sort_values(self._index, ascending=False)[:][:num_cols]

        # Extract column names and corresponding values
        columns = d.index.tolist()
        values = d.loc[:, self._index].tolist()

        # Add the normal metric diagram
        self._diagrams.addWidget(self.generate_diagram(columns, values, f'{self._name} {self._index}'))

    def generate_diagram(self, columns: list[str], values: list[float], name: str, limit: int = 1) -> FigureCanvasQTAgg:
        """
        Generate a diagram with the given columns and values
        :param columns: labels to display in the x-axis
        :param values: values to display in the y-axis, with the bars
        :param name: name of the diagram
        :param limit: limit of the y-axis
        :return: FigureCanvasQTAgg with the diagram
        """
        # Set the color of the selected column
        colors: list[str] = [BAR_COLOR if self._selected_column != c else SELECTED_COLOR for c in columns]

        # Plotting
        plt.figure()  # Adjust figure size as needed
        plt.bar(columns, values, color=colors)

        # Add color to the selected column
        mplcursors.cursor(plt.gcf(), hover=2)
        mplcursors.cursor(plt.gcf()).connect("add", lambda sel: (
            sel.annotation.set_visible(False),
            setattr(self, '_selected_column', sel.annotation.get_text().split('\n')[0].split('=')[1]
            if getattr(self, '_selected_column', NOT_SELECTECTED) != sel.annotation.get_text()
                    .split('\n')[0].split('=')[1] else NOT_SELECTECTED),
            self.update_diagrams(),
            self.start_animation()
        ))

        # Customize plot
        plt.xlabel('Column Names')
        plt.ylabel('Values')
        plt.ylim(0, limit)
        plt.title(name)
        # remove column labels if there are too many columns
        if len(columns) > 50:
            plt.xticks([])
        else:
            plt.xticks(rotation=45)
        plt.tight_layout()

        return FigureCanvasQTAgg(plt.gcf())

    def update_diagrams(self, num_cols: int = -1) -> None:
        """
        Update the diagrams with the new data
        :param num_cols: number of columns to display, -1 to use the current value (unknown at the moment of the call)
        :return: None
        """
        # Clear the existing diagrams
        self._layout.removeWidget(self._diagrams)
        self._diagrams.deleteLater()
        plt.close('all')

        # Regenerate the diagram with updated data
        self._diagrams = QSplitter(Qt.Horizontal, self)

        # Get the number of columns to display
        if num_cols == -1:
            num_cols = self._num_col_box.value()
        # Generate the diagrams
        self.generate_diagrams(num_cols)

        # Update the canvas widget with the new diagrams
        self._layout.insertWidget(3, self._diagrams, stretch=1)

    def reset(self) -> None:
        """
        Reset the page to its initial state
        :return: None
        """
        self.stop_animation()
        self._num_col_box.setValue(COLS)
