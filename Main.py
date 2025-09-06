from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget, QGridLayout, QLabel, QPushButton, QSizePolicy, QScrollArea, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
import sys
from utils import FileUtils, ClipboardUtils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CharPalette')
        self.setWindowIcon(QIcon('assets/charpalette-logo.ico'))
        self.setFixedSize(464, 600)
        self.tray_icon: QSystemTrayIcon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('assets/charpalette-logo.ico'))
        self.tray_icon.setToolTip('CharPalette')

        # Setup system tray icon
        self.setup_tray_icon()

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

        # Load emoji from file using utility function
        emoji_list: list[str] = FileUtils.load_emojis_from_file('assets/emoji.txt')

        # Setup grid layout for each tab
        self.setup_grid_for_tab(emoji_tab, 'Emoji Grid', emoji_list)
        self.setup_grid_for_tab(math_tab, 'Math Symbols Grid')
        self.setup_grid_for_tab(punctuation_tab, 'Punctuations Grid')

        # Set the central widget of the Window.
        self.setCentralWidget(tabs)

    def setup_tray_icon(self) -> None:
        """Setup system tray icon."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        # Create context menu for tray icon
        tray_menu: QMenu = QMenu()

        # Show/Hide action
        show_action: QAction = QAction('Show CharPalette', self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        # Quit action
        quit_action: QAction = QAction('Quit', self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # Connect double-click to show window
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Show tray icon
        self.tray_icon.show()

    def tray_icon_activated(self, reason) -> None:
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()

    def show_window(self) -> None:
        """Show and bring window to front."""
        self.show()
        self.raise_()
        self.activateWindow()

    def quit_application(self) -> None:
        """Quit the application completely."""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        QApplication.instance().quit()

    def closeEvent(self, event) -> None:
        """Override close event to minimize to tray instead of quitting."""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
            if not hasattr(self, '_first_minimize_shown'):
                self.tray_icon.showMessage(
                    'CharPalette',
                    'Application was minimized to tray',
                    QSystemTrayIcon.MessageIcon.Information,
                    2000
                )
                self._first_minimize_shown: bool = True
        else:
            event.accept()


    def setup_grid_for_tab(self, tab_widget, placeholder_text, emoji_list=None) -> None:
        """Helper function to create a grid layout in a tab."""
        # Create scroll area for the tab
        scroll_area: QScrollArea = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Create content widget for the scroll area
        content_widget: QWidget = QWidget()
        layout: QGridLayout = QGridLayout(content_widget)
        layout.setHorizontalSpacing(4)
        layout.setVerticalSpacing(4)
        layout.setContentsMargins(10, 10, 10, 10)

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
                btn.clicked.connect(lambda checked, e=emoji: ClipboardUtils.copy_to_clipboard(e))
                layout.addWidget(btn, row, col)
        else:
            # Add a placeholder label to show something is there
            label: QLabel = QLabel(placeholder_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label, 0, 0)

        # Set the content widget to scroll area
        scroll_area.setWidget(content_widget)

        # Add scroll area to tab widget
        tab_layout: QGridLayout = QGridLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll_area, 0, 0)

if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    app.setApplicationName('CharPalette')
    with open('CharPalette.qss', 'r') as f:
        app.setStyleSheet(f.read())
    window: QMainWindow = MainWindow()
    window.show()
    app.exec()
