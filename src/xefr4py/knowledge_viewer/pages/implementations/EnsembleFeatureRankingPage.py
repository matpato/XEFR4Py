import function
import pandas
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QFont
from pandas import DataFrame

from Utils import get_log_dir
from xefr4py.knowledge_viewer.pages.block_diagram.implementations import EnsembleFeatureRankingBlockDiagramScene
from xefr4py.knowledge_viewer.pages.block_diagram import BlockDiagramView, BlockDiagramScene
from xefr4py.knowledge_viewer.pages.table import PandasTableView
from xefr4py.knowledge_viewer.pages import ChildPageWithBlockDiagram

"""
This class is a child page that displays the blocks diagram of the ensemble feature ranking.
It displays a table with the execution time and the block diagram.
"""


LOG_DIR: str = get_log_dir()
FILE: str = f'{LOG_DIR}/EEFR.tsv'


class EnsembleFeatureRankingPage(ChildPageWithBlockDiagram):
    _table_info: PandasTableView

    def __init__(self, font: QFont, margins: QMargins, line_thickness: int, button_parent_func: function) -> None:
        blockDiagram: BlockDiagramScene = EnsembleFeatureRankingBlockDiagramScene(font, line_thickness)
        view: BlockDiagramView = BlockDiagramView(blockDiagram)
        super().__init__(font, margins, 'Enhanced Ensemble Feature Ranking', view, button_parent_func)

        # Load the data
        info: DataFrame = pandas.read_csv(FILE, sep='\t')

        # Create the table and add it to the layout
        self._table_info = PandasTableView(self, info.T, font)
        self._layout.insertWidget(1, self._table_info)
