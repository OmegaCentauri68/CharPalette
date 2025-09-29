# main.py
from PySide6.QtCore import Qt, QSize, QMargins, QPoint, QRect
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QFrame, QTabWidget, QGridLayout
from PySide6.QtGui import QGuiApplication
import sys
from utils import *

YAML_PATH: str = 'assets/config/tabs.yaml'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CharPalette')

        # Create Central Widget
        central_widget, central_layout = create_widget(QWidget, layout_class=QHBoxLayout, object_name='centralWidget')
        central_layout.setContentsMargins(0, 0, 0, 0); central_layout.setSpacing(0)
        self.setCentralWidget(central_widget)

        # Create Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)

        # Add Tabs To Central Widget
        self.add_tabs(get_yaml_data(YAML_PATH))
        central_layout.addWidget(self.tabs)

    def add_tabs(self, yaml_data: list[TabConfig]) -> None:
        for tab in yaml_data:
            symbol_tab = SymbolTab(tab['path'])
            self.tabs.addTab(symbol_tab, tab['tab_name'])

class SymbolTab(QFrame):
    def __init__(self, file_path: str):
        super().__init__()
        self.setObjectName('symbolTab')
        self.layout = FlowLayout(self)
        self.layout.setSpacing(0)
        self.add_symbol_buttons(get_tab_file_data(file_path))

    def add_symbol_buttons(self, symbol_list: tuple[str, ...]) -> None:
        for symbol in symbol_list:
            button = create_widget(QPushButton, text=symbol, object_name='symbolButton')
            button.setFixedWidth(button.sizeHint().height())
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked, s=symbol: QGuiApplication.clipboard().setText(s))
            self.layout.addWidget(button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    load_qss(app, 'assets/styles.qss')
    window = MainWindow()
    window.resize(400, 600)
    window.show()
    app.exec()