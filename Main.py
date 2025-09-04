from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CharPalette')

        # Create the main tab widget
        tabs: QTabWidget = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.South)
        tabs.setDocumentMode(True)

        # Create a widget for each tab
        emoji_tab: QWidget = QWidget()
        math_tab: QWidget = QWidget()
        punctuation_tab: QWidget = QWidget()

        # Add tabs to the tab widget
        tabs.addTab(emoji_tab, 'Emoji')
        tabs.addTab(math_tab, 'Math Symbols')
        tabs.addTab(punctuation_tab, 'Punctuations')

        # Setup grid layout for each tab
        self.setup_grid_for_tab(emoji_tab, 'Emoji Grid')
        self.setup_grid_for_tab(math_tab, 'Math Symbols Grid')
        self.setup_grid_for_tab(punctuation_tab, 'Punctuations Grid')

        # Set the central widget of the Window.
        self.setCentralWidget(tabs)

    def setup_grid_for_tab(self, tab_widget, placeholder_text):
        """Helper function to create a grid layout in a tab."""
        layout: QGridLayout = QGridLayout(tab_widget)
        # Add a placeholder label to show something is there
        label: QLabel = QLabel(placeholder_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, 0, 0)

if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    app.setApplicationName('CharPalette')
    window: QMainWindow = MainWindow()
    window.resize(800, 600)
    window.show()
    with open('CharPalette.qss', 'r') as f:
        app.setStyleSheet(f.read())
    app.exec()