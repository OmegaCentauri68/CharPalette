# utils.py
from typing import TypeVar, overload
from PySide6.QtCore import QSize, Qt, QObject, QMargins, QPoint, QRect
from PySide6.QtWidgets import QApplication, QLayout, QFrame, QWidget, QSizePolicy
from typing import TypedDict
from grapheme import graphemes
import yaml

T = TypeVar('T', bound=QWidget)
L = TypeVar('L', bound=QLayout)

class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
            )
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()

class TabConfig(TypedDict):
    tab_name: str
    font: str
    path: str

@overload
def create_widget(widget_class: type[T], layout_class: None = None, text: str|None = None, object_name: str|None = None) -> T: ...
@overload
def create_widget(widget_class: type[T], layout_class: type[L], text: str|None = None, object_name: str|None = None) -> tuple[T, L]: ...

def create_widget(widget_class: type[T], layout_class: type[L]|None = None, text: str|None = None, object_name: str|None = None) -> T | tuple[T, L]:
    """Quickly create widget and set layout"""
    widget = widget_class()
    if layout_class is not None:
        layout = layout_class()
        widget.setLayout(layout)
    if object_name is not None: widget.setObjectName(object_name)
    if text is not None and hasattr(widget, 'setText'):
        widget.setText(text)

    if layout_class:
        return widget, layout
    else:
        return widget

def create_layout(widget: QWidget, layout_class: type[L]) -> L:
    """Quickly create and set layout"""
    layout = layout_class()
    widget.setLayout(layout)
    return layout

def add_widgets(self: QLayout, *widgets: QWidget) -> None:
    for widget in widgets:
        self.addWidget(widget)

def set_objects_name(names: dict[QWidget, str]) -> None:
    for widget, name in names.items():
        widget.setObjectName(name)

def load_qss(app: QApplication, file_path: str) -> None:
    with open(file_path, 'r') as file:
        app.setStyleSheet(file.read())

def get_yaml_data(file_path: str) -> list[TabConfig]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: List[TabConfig] = yaml.safe_load(file)
    return data

def get_tab_file_data(file_path: str) -> tuple[str, ...]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content: str = f.read()
        return tuple(g for g in graphemes(content) if not g.isspace())

QLayout.add_widgets = add_widgets

if __name__ == '__main__':
    print(get_tab_file_data('assets/tabs/emojis.txt'))