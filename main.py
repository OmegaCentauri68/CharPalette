# main.py
from PySide6.QtCore import Qt, QSize, QMargins, QPoint, QRect
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QFrame, QSpacerItem, QScrollArea
from PySide6.QtGui import QGuiApplication, QFont
import sys
from utils import *

QWIDGETSIZE_MAX: int = 16777215
YAML_PATH: str = 'assets/config/tabs.yaml'
YAML_DATA: list[TabConfig]

class Header(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('header')
        layout = create_layout(self, QHBoxLayout)
        layout.setSpacing(0); layout.setContentsMargins(0, 0, 0, 0)
        self.setting_button = create_widget(QPushButton, text='Setting', object_name='headerButton')
        self.edit_button = create_widget(QPushButton, text='Edit', object_name='headerButton')
        self.change_font_button = create_widget(QPushButton, text='Font', object_name='headerButton')

        self.style_buttons((self.setting_button, self.edit_button, self.change_font_button))
        layout.addWidget(self.setting_button)
        layout.addStretch()
        layout.add_widgets(self.edit_button, self.change_font_button)
        layout.setAlignment(Qt.AlignTop)

    def style_buttons(self, button_list: tuple) -> None:
        for button in button_list:
            button.setFixedWidth(50)
            button.setFlat(True)
            button.setCursor(Qt.PointingHandCursor)

class Footer(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('footer')
        self.layout = create_layout(self, QHBoxLayout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.add_tab_buttons()

    @staticmethod
    def on_button_toggled(checked: bool, button: QPushButton, name: str) -> None:
        global current_tab, tabs, tab_buttons
        if name == current_tab: return

        # Toggle Tab Buttons
        for button in tab_buttons:
            if button.text() == name:
                button.setEnabled(False)
                change_font_weight(button, QFont.Bold)
                continue
            button.setChecked(False)
            button.setEnabled(True)
            change_font_weight(button, QFont.Normal)

        # Switch Tabs
        for tab in tabs:
            if tab.widget().name == name:
                tab.setMaximumWidth(QWIDGETSIZE_MAX)
                current_tab = tab.widget().name
            else:
                tab.setMaximumWidth(0)

    def add_tab_buttons(self):
        global tab_buttons
        for tab_dict in YAML_DATA:
            button = create_widget(QPushButton, text=tab_dict['tab_name'], object_name='tabButton')
            button.setFlat(True); button.setCursor(Qt.PointingHandCursor)
            button.setCheckable(True)
            button.toggled.connect(lambda checked, btn=button, name=tab_dict['tab_name']: self.on_button_toggled(checked, btn, name))
            self.layout.addWidget(button)
            tab_buttons.append(button)
        self.layout.addStretch()

class SymbolTab(QFrame):
    def __init__(self, file_path: str):
        super().__init__()
        self.setObjectName('symbolTab')
        self.layout = FlowLayout(self)
        self.layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.add_symbol_buttons(get_tab_file_data(file_path))

        self.name: str = ''
        self.font = QFont()

    def add_symbol_buttons(self, symbol_list: tuple[str, ...]) -> None:
        for symbol in symbol_list:
            button = create_widget(QPushButton, text=symbol, object_name='symbolButton')
            button.setFixedHeight(button.sizeHint().height() + 12)
            button.setFixedWidth(button.sizeHint().height() + 12); button.setFlat(True); button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked, s=symbol: QGuiApplication.clipboard().setText(s))
            self.layout.addWidget(button)

    def heightForWidth(self, width: int) -> int:
        return self.layout.heightForWidth(width)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global YAML_DATA
        YAML_DATA = get_yaml_data(YAML_PATH)
        self.setWindowTitle('CharPalette')

        # Create Central Widget
        central_widget, central_layout = create_widget(QWidget, layout_class=QVBoxLayout, object_name='centralWidget')
        central_layout.setContentsMargins(0, 0, 0, 0);
        central_layout.setSpacing(0)
        self.setCentralWidget(central_widget)

        # Add Header
        header = Header()

        # Add Tab Container
        self.tabs_container, self.tabs_container_layout = create_widget(QWidget, layout_class=QHBoxLayout, object_name='tabsContainer')
        self.tabs_container_layout.setContentsMargins(0, 0, 0, 0); self.tabs_container_layout.setSpacing(0)
        self.tabs_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.add_tabs()

        # Add Footer
        footer = Footer()

        self.clean_up()
        central_layout.add_widgets(header, self.tabs_container, footer)

    def add_tabs(self) -> None:
        global current_tab, tabs
        for tab_dict in YAML_DATA:
            symbol_tab = SymbolTab(tab_dict['path'])
            symbol_tab.name = tab_dict['tab_name']

            scroll_area = QScrollArea()
            scroll_area.setWidget(symbol_tab)
            scroll_area.setWidgetResizable(True)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setObjectName('symbolTabScrollArea')

            scroll_area.name = tab_dict['tab_name']
            self.tabs_container_layout.addWidget(scroll_area)
            tabs.append(scroll_area)
            scroll_area.setMaximumWidth(0)
        current_tab = YAML_DATA[0]['tab_name']
        for tab in tabs:
            if tab.widget().name == current_tab:
                tab.setMaximumWidth(QWIDGETSIZE_MAX)
                break

    @staticmethod
    def clean_up():
        global current_tab, tab_buttons
        for button in tab_buttons:
            if button.text() == current_tab:
                button.setChecked(True)
                button.setEnabled(False)
                change_font_weight(button, QFont.Bold)
                break

current_tab: str = ''
tabs: list[QScrollArea] = []
tab_buttons: list[QPushButton] = []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    load_qss(app, 'styles.qss')
    window = MainWindow()
    window.resize(400, 600)
    window.show()
    app.exec()