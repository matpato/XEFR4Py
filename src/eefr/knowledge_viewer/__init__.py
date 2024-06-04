import sys

import function
import pandas
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QFont, QResizeEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout

from eefr.knowledge_viewer.Page.BasePage import BasePage
from eefr.knowledge_viewer.Page.implementations.CalculateRankSamplingPage import CalculateRankSamplingPage
from eefr.knowledge_viewer.Page.implementations.CalculateWeightsSamplingPage import CalculateWeightsSamplingPage
from eefr.knowledge_viewer.Page.implementations.ConstructorPage import ConstructorPage
from eefr.knowledge_viewer.Page.implementations.DiscretizerPage import DiscretizerPage
from eefr.knowledge_viewer.Page.implementations.EnsembleFeatureRankingPage import EnsembleFeatureRankingPage
from eefr.knowledge_viewer.Page.implementations.GetNRandomRowsSubsetsPage import GetNRandomRowsSubsetsPage
from eefr.knowledge_viewer.Page.implementations.MainPage import MainPage
from eefr.knowledge_viewer.Page.implementations.MetricPage import MetricPage
from Utils import get_list_from_str

"""
This file is the main file for the knowledge viewer. 
It creates the main window and the stacked widget to manage the pages.
"""

LOG_PATH: str = "../../logs"

MARGIN_PERCENTAGE: float = 0.05

LINE_THICKNESS: int = 3

BACKGROUND_COLOR: str = 'white'


class KnowledgeViewerWindow(QMainWindow):
    _layout: QVBoxLayout
    _stacked_widget: QStackedWidget

    # Pages
    _main: MainPage
    _constructor: ConstructorPage
    _ensemble_feature_ranking: EnsembleFeatureRankingPage
    _get_n_random_rows_subsets: GetNRandomRowsSubsetsPage

    def __init__(self) -> None:
        super().__init__()
        # Set background color for the main window
        self.setStyleSheet(f'QMainWindow {{ background-color: {BACKGROUND_COLOR}; }}')

        # Create a widget for layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the main window
        self._layout = QVBoxLayout(self.central_widget)
        self._layout.setAlignment(Qt.AlignTop)

        font: QFont = QFont("Arial", 12)

        # Calculate margins based on window size
        window_width = self.width()
        window_height = self.height()
        margins: QMargins = QMargins(int(window_width * MARGIN_PERCENTAGE),
                                     int(window_height * MARGIN_PERCENTAGE),
                                     int(window_width * MARGIN_PERCENTAGE),
                                     int(window_height * MARGIN_PERCENTAGE)
                                     )
        self._layout.setContentsMargins(margins)

        # Create a stacked widget to manage pages
        self._stacked_widget = QStackedWidget(self.central_widget)
        self._layout.addWidget(self._stacked_widget)

        # main page
        self._main = MainPage(font, margins, LINE_THICKNESS)
        self._stacked_widget.addWidget(self._main)

        # constructor page
        self._constructor = ConstructorPage(font, margins, lambda: self.show_page(self._main))
        self._stacked_widget.addWidget(self._constructor)

        # ensemble feature ranking page
        self._ensemble_feature_ranking = EnsembleFeatureRankingPage(
            font, margins, LINE_THICKNESS, lambda: self.show_page(self._main))
        self._stacked_widget.addWidget(self._ensemble_feature_ranking)

        # get n random rows subsets page
        self._get_n_random_rows_subsets = GetNRandomRowsSubsetsPage(
            font, margins, lambda: self.show_page(self._ensemble_feature_ranking))
        self._stacked_widget.addWidget(self._get_n_random_rows_subsets)

        # calculate weights sampling page
        self.calculate_weights_sampling = CalculateWeightsSamplingPage(
            font, margins, lambda: self.show_page(self._ensemble_feature_ranking))
        self._stacked_widget.addWidget(self.calculate_weights_sampling)

        # create discretizer page
        self.discretizer = DiscretizerPage(font, margins, lambda: self.show_page(self._constructor))
        self._stacked_widget.addWidget(self.discretizer)

        # create the metrics pages
        metrics: list[str] = get_list_from_str(
            pandas.read_csv(f'{LOG_PATH}/calculate_weights_sampling.tsv', sep='\t')['Metrics'][0])
        self.metrics = []
        for metric in metrics:
            self.metrics.append(MetricPage(
                font, margins, metric, lambda: self.show_page(self.calculate_weights_sampling)))
            self._stacked_widget.addWidget(self.metrics[-1])

        # calculate rank sampling page
        self.calculate_rank_sampling = CalculateRankSamplingPage(
            font, margins, lambda: self.show_page(self._ensemble_feature_ranking))
        self._stacked_widget.addWidget(self.calculate_rank_sampling)

        # Inject the button functions
        self._main.inject_funcs([lambda: self.show_page(self._constructor),
                                 lambda: self.show_page(self._ensemble_feature_ranking)])

        self._constructor.inject_funcs([lambda: self.show_page(self.discretizer)])

        self._ensemble_feature_ranking.inject_funcs([lambda: self.show_page(self._get_n_random_rows_subsets),
                                                     lambda: self.show_page(self.calculate_weights_sampling),
                                                     lambda: self.show_page(self.calculate_rank_sampling)])

        metric_funcs = [self.create_func(metric) for metric in self.metrics]
        self.calculate_weights_sampling.inject_funcs(metric_funcs)

        # Set the window properties
        self.setWindowTitle("Ensemble Feature Ranking Knowledge Viewer")
        self.resize(1280, 720)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        This function is called when the window is resized.
        It updates the margins of the layout based on the new window.
        :param event: QResizeEvent with the new window size
        :return: None
        """
        # Update the margins based on the new window size
        window_width = event.size().width()
        window_height = event.size().height()
        margins: QMargins = QMargins(int(window_width * MARGIN_PERCENTAGE),
                                     int(window_height * MARGIN_PERCENTAGE),
                                     int(window_width * MARGIN_PERCENTAGE),
                                     int(window_height * MARGIN_PERCENTAGE)
                                     )
        self._layout.setContentsMargins(margins)
        super().resizeEvent(event)

    def show_page(self, page: BasePage) -> None:
        """
        This function is called to switch to the specified page in the stacked widget.
        :param page: page to switch to
        :return: None
        """
        # Switch to the specified page in the stacked widget
        index = self._stacked_widget.indexOf(page)
        self._stacked_widget.setCurrentIndex(index)

    def create_func(self, metric: MetricPage) -> function:
        return lambda: self.show_page(metric)


def launch_dashboard():
    app: QApplication = QApplication([])
    window: QMainWindow = KnowledgeViewerWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    launch_dashboard()
    print("Hello World")
