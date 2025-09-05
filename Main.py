from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget, QGridLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QIcon
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CharPalette')
        self.setWindowIcon(QIcon('assets/charpalette-logo.ico'))

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

        # Load emoji from file
        emoji_list: list[str] = self.load_emojis_from_file('emoji.txt')

        # Setup grid layout for each tab
        self.setup_grid_for_tab(emoji_tab, 'Emoji Grid', emoji_list)
        self.setup_grid_for_tab(math_tab, 'Math Symbols Grid')
        self.setup_grid_for_tab(punctuation_tab, 'Punctuations Grid')

        # Set the central widget of the Window.
        self.setCentralWidget(tabs)

    def load_emojis_from_file(self, filename: str) -> list[str]:
        """Load emojis from a txt file. Each character in the file becomes an emoji."""
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            # Convert string to list of characters (each emoji is a character)
            return list(content)

    def setup_grid_for_tab(self, tab_widget, placeholder_text, emoji_list=None) -> None:
        """Helper function to create a grid layout in a tab."""
        layout: QGridLayout = QGridLayout(tab_widget)
        layout.setHorizontalSpacing(4)
        layout.setVerticalSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        if emoji_list:
            cols: int = 10
            for idx, emoji in enumerate(emoji_list):
                row: int = idx // cols
                col: int = idx % cols
                btn: QPushButton = QPushButton(emoji)
                btn.setObjectName('emojiButton')
                btn.setFlat(True)
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
                btn.clicked.connect(lambda checked, e=emoji: self.copy_to_clipboard(e))
                layout.addWidget(btn, row, col)
            layout.setRowStretch(layout.rowCount(), 1)
        else:
            # Add a placeholder label to show something is there
            label: QLabel = QLabel(placeholder_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label, 0, 0)

    def copy_to_clipboard(self, text) -> None:
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(text)

if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    app.setApplicationName('CharPalette')
    window: QMainWindow = MainWindow()
    window.resize(800, 600)
    window.show()
    with open('CharPalette.qss', 'r') as f:
        app.setStyleSheet(f.read())
    app.exec()